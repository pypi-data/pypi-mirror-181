from math import ceil
import time
import os
import re

import numpy as np
from geodesic.account.projects import _ProjectDescr, get_active_project
from geodesic.descriptors import _BBoxDescr, _GeometryDescr, _IntDescr, _ListDescr, \
    _StringDescr, _TypeConstrainedDescr
from geodesic.service import ServiceClient
from geodesic.tesseract.components import AssetSpecListDescr, GlobalProperties, JobResponse, Step, Bucket, Webhook
from geodesic.utils import DeferredImport, MockImport
from geodesic.bases import _APIObject
from geodesic.client import raise_on_error
from geodesic import Dataset
from geodesic.stac import FeatureCollection, Item


tqdm = DeferredImport('tqdm')
ipywidgets = DeferredImport('ipywidgets')
ipyleaflet = DeferredImport('ipyleaflet')
display = DeferredImport('IPython.display')
nx = DeferredImport('networkx')

try:
    import zarr
except ImportError:
    zarr = MockImport("zarr")


job_id_re = re.compile(r'job_id=(\w*)')


class Job(_APIObject):
    """represents a Tesseract Job

    The class can be initialized either with a dictionary (\\*\\*spec) that represents the request for the particular
    type, or can be given an job ID. If a job ID is provided it will query for that job on the tesseract service
    and then update this class with the specifics of that job.

    Args:
        \\*\\*spec: A dictionary representing the job request.
        job_id: The job ID string. If provided the job will be initialized
            with info by making a request to tesseract.
    """

    name = _StringDescr(doc="a unique name for the dataset created by this job.")
    alias = _StringDescr(doc="a human readable name for the dataset created by this job")
    description = _StringDescr(doc="a longer description for the dataset created by this job")
    project = _ProjectDescr(doc="the project that this job will be assigned to")
    workers = _IntDescr(doc="the number of workers to use for this job")
    bbox = _BBoxDescr(doc="the rectangular extent of this job. Can be further filtered by a geometry")
    bbox_epsg = _IntDescr(doc="the EPSG code of the bounding box spatial reference")
    output_epsg = _IntDescr(
        doc="the EPSG code of the output spatial reference. Pixel size will be with respect to this")
    geometry = _GeometryDescr(doc="a geometry to filter the job with only assets intersecting this will be processed")
    global_properties = _TypeConstrainedDescr(
        (GlobalProperties, dict),
        doc="properties applied to unspecified fields in an asset spec")
    asset_specs = AssetSpecListDescr(doc="the initial assets to compute in the job")
    workers = _IntDescr(doc="number of workers to use for each step in the job")
    steps = _ListDescr(item_type=(Step, dict), doc="a list of steps to execute", coerce_items=True)
    hooks = _ListDescr(item_type=(Webhook, dict), doc="a list of webhooks to execute when job is complete")
    output = _TypeConstrainedDescr((Bucket, dict), doc="the output, other than default storage")

    def __init__(self, job_id: str = None, **spec):
        self.project = get_active_project()
        self._submitted = False
        self._dataset = None
        self._item = None
        self._bounds = None
        self._widget = None

        self._service = ServiceClient("tesseract", 1)

        # status values
        self._state = None
        self._n_quarks = None
        self._n_completed = None

        # geometries
        self._query_geom = None
        self._quark_geoms = None
        self.job_id = None

        if job_id is not None:
            self.load(job_id=job_id)

        super().__init__(**spec)

    def load(self, job_id: str, dry_run: bool = False) -> None:
        """Loads job information for `job_id` if the job exists
        """
        job_resp = raise_on_error(self._service.get(f'jobs/{job_id}', project=self.project.uid)).json()
        self.update(job_resp['jobs'][0])
        self.job_id = job_id

        if dry_run:
            return

        # If this isn't a dry run, load the other data.
        ds = raise_on_error(self._service.get(f'jobs/{job_id}/dataset')).json()
        self._dataset = Dataset(**ds)
        si = raise_on_error(self._service.get(f'jobs/{job_id}/item')).json()
        self._item = Item(**si)
        self._query_geom = getattr(self._item, 'geometry', None)
        self.status(return_quark_geoms=True)

    def submit(self, overwrite: bool = False, dry_run: bool = False, timeout_seconds: float = 30.0) -> JobResponse:
        """Submits a job to be processed by tesseract

        This function will take the job defined by this class and submit it to the tesseract api for processing.
        Once submitted the dataset and items fields will be populated containing the SeerAI dataset and STAC item
        respectively. Keep in mind that even though the links to files in the STAC item will be populated, the job
        may not yet be completed and so some of the chunks may not be finished.

        Args:
            overwrite: if the job exists, deletes it and creates a new one
            dry_run: runs this as a dry run (no work submitted, only estimated.)
        """

        # If this job has a job_id, delete the existing job
        if self.job_id is not None:
            if overwrite:
                self.delete_and_wait()
            else:
                self.status()
                # If the current job state is "dry_run" and we're submitting a non-dry run, delete the job and wait.
                if self.state == 'dry_run' and not dry_run:
                    self.delete_and_wait(timeout_seconds=timeout_seconds)
                else:
                    self.load(self.job_id, dry_run=self.state == "dry_run")
                    return

        req = dict(self)
        req['dry_run'] = dry_run

        # submit the job
        response = self._service.post("submit", **req)

        res = response.json()
        # If there's an error, get the job ID from that error
        if 'error' in res:
            detail = res['error'].get('detail', '')
            job_id_match = job_id_re.search(detail)
            # If the job already exists and we don't already have the job_id set, get and set the job_id
            if 'exists' in detail and job_id_match and self.job_id is None:
                job_id = job_id_match.group(1)
                self.job_id = job_id

                # Recursively call this, now that we have the job_id
                return self.submit(overwrite=overwrite, dry_run=dry_run, timeout_seconds=timeout_seconds)
            else:
                raise_on_error(response)

        res = JobResponse(**res)

        job_id = res.get("job_id", None)
        if job_id is None:
            raise ValueError("no job_id was returned, something went wrong")

        self.job_id = job_id
        self.load(job_id, dry_run=dry_run)
        self._submitted = True

        res.warn()
        return res

    def delete_and_wait(self, timeout_seconds=30.0):
        self.delete(remove_data=True)
        timeout = time.time() + timeout_seconds
        timed_out = True
        while time.time() < timeout:
            self.status()
            if self._state == "deleted":
                timed_out = False
                break
            time.sleep(1.0)
        if timed_out:
            raise ValueError("Job submission timed out waiting for deletion to complete. Job is still deleting,"
                             " please try again later")

    @property
    def dataset(self):
        return self._dataset

    @property
    def item(self):
        return self._item

    @property
    def state(self):
        return self._state

    def zarr(self, asset_name: str = None):
        """
        Returns the Zarr group for the corresponding asset name

        Args:
            asset_name: name of the asset to open and return
        Returns:
            zarr file pointing to the results.
        """
        if self._item is None or self._n_completed != self._n_quarks:
            raise ValueError("computation not completed")

        try:
            assets = self._item.assets
        except AttributeError:
            raise AttributeError("item has no assets")

        try:
            asset = assets[asset_name]
        except KeyError:
            raise KeyError(f"asset {asset_name} does not exist")

        href = asset.href

        return zarr.open(href)

    def ndarray(self, asset_name: str):
        """
        Returns a numpy.ndarray for specified asset name.

        USE WITH CAUTION! RETURNS ALL OF WHAT COULD BE A
        HUGE ARRAY

        Args:
            asset_name: name of the asset to open and return
        Returns:
            numpy array of all the results.
        """
        return self.zarr(asset_name)['tesseract'][:]

    def status(self, return_quark_geoms: bool = False, return_quark_status: bool = False):
        """Status queries the tesseract service for the jobs status.

        Args:
            return_quark_geoms(bool): Should the query to the service ask for all of the quarks geometries.
                                    If True it will populate the geometry in this class.
            return_quark_status(bool): If True will query for the status of each individual quark associated with
                                    the job.

        Returns:
            A dictionary with the response from the Tesseract service

        """

        if not self.job_id:
            raise Exception("job_id not set, cannot get status")

        q = {
            "return_quark_geoms": return_quark_geoms,
            "return_quark_status": return_quark_status
        }
        res = raise_on_error(self._service.get(f'jobs/{self.job_id}/status', **q)).json()

        status = res.get('job_status', None)
        if status is None:
            print(res)
            raise Exception("could not get job status")

        self._n_quarks = status.get('n_quarks', None)
        self._n_completed = status.get('n_quarks_completed', 0)
        self._state = status.get('state', None)

        if return_quark_geoms:
            quark_geoms = status.get('features', None)
            if quark_geoms is None:
                raise Exception("job status returned no geometries")
            self.quark_geoms = FeatureCollection(**quark_geoms)

        self._status = status
        return status

    def add_step(self, step: Step):
        self.steps.append(Step(**step))

    def delete(self, remove_data: bool = False):
        """Deletes a job in the Tesseract service.

        Unless specified, data created by this job will remain in the underyling storage. Set
        `remove_data` to True to remove created asset data.

        Args:
            remove_data: Delete underyling data created by this job
        """

        if not self.job_id:
            raise Exception("job_id not set, cannot delete")

        _ = raise_on_error(self._service.delete(f'jobs/{self.job_id}', remove_data=remove_data)).json()
        self._submitted = False

    @property
    def dag(self):
        graph = nx.Graph()
        for asset in self.asset_specs:
            graph.add_node(asset.name)

        # add asset/step nodes and asset/step and step/asset edges
        for step in self.steps:
            graph.add_node(step.name, type="step", color="red")
            for input in step.inputs:
                if input.get('asset_name') is not None:
                    graph.add_node(input.asset_name, type="asset", color="green")
                    graph.add_edge(input.asset_name, step.name)
            for output in step.outputs:
                graph.add_node(output.asset_name, type="asset")
                graph.add_edge(step.name, output.asset_name)

        return graph

    def _build_widget(self, basemap=None):

        # Progress bar
        self._prog = ipywidgets.IntProgress(
            value=self._n_completed,
            min=0,
            max=self._n_quarks,
            step=1,
            description="Running: ",
            bar_style='',
            orientation='horizontal'
        )
        self._title = ipywidgets.HTML(
            value=self._get_title()
        )
        self._ratio = ipywidgets.HTML(
            value=self._get_ratio()
        )

        zoom, center, _ = self._calc_zoom_center()

        if basemap is None:
            basemap = ipyleaflet.basemaps.CartoDB.DarkMatter

        self.map = ipyleaflet.Map(
            basemap=basemap,
            center=center,
            zoom=zoom,
        )

        self.map.add_control(ipyleaflet.LayersControl(position='topright'))

        vb = ipywidgets.VBox([self._title, self._ratio, self._prog])
        w = ipywidgets.HBox([vb, self.map])
        self._widget = w

    def _add_item_layer(self):
        if not self._item:
            return

        disp = Item(**self._item)
        disp.geometry = disp.geometry.buffer(np.sqrt(disp.geometry.area) * 0.05).envelope
        fci = {
            'type': 'FeatureCollection',
            'features': [
                disp
            ]
        }
        query_layer = ipyleaflet.GeoJSON(
            data=fci,
            style={
                "opacity": 1, "color": "#e2e6d5", "fillOpacity": 0.0, 'weight': 1, "dashArray": "4 4"
            },
            hover_style={
                'fillOpacity': 0.75
            }
        )
        query_layer.name = "Requested Extent"
        self.map.add_layer(query_layer)

    def _add_quark_layer(self):

        if not self.quark_geoms:
            return

        fc = {
            'type': 'FeatureCollection',
            'features': self.quark_geoms.features
        }
        self._quark_layer = ipyleaflet.GeoJSON(
            data=fc,
            style={
            },
            hover_style={
                'fillOpacity': 0.75,
            },
            style_callback=self._quark_style,
        )
        self._quark_layer.name = "Quark Extents"
        self.map.add_layer(self._quark_layer)

    def widget(self, basemap=None):
        try:
            ipywidgets.VBox
        except ImportError:
            raise ValueError("ipywidgets must be installed to view widget")

        if self._state == "dry_run":
            return ipywidgets.HTML(
                value='<h2 style="color: red;">Job is currently in "dry_run" state. Submit before watching job</h2>'
            ), False

        if not self.job_id:
            raise Exception("job_id not set, nothing to watch")

        self.quark_geoms_lookup = {}
        for q in self.quark_geoms.features:
            self.quark_geoms_lookup[q['id']] = q

        quark_status = self.status(return_quark_status=True)
        for k, status in quark_status['quark_status'].items():
            self.quark_geoms_lookup[k].properties['status'] = status

        self._build_widget(basemap=basemap)
        self._add_item_layer()
        self._add_quark_layer()
        return self._widget, True

    def _quark_style(self, feature):
        # Default Style
        style = {
            "opacity": 0.5,
            "color": "#888888",
            "fillColor": "#888888",
            "fillOpacity": 0.05
        }

        sts = feature['properties'].get('status', 'incomplete')
        if sts == "incomplete":
            style['fillOpacity'] = 0.0
            return style
        elif sts == "running":
            style['fillColor'] = 'yellow'
            style['color'] = 'yellow'
            style['opacity'] = 1.0
        elif sts == "failed":
            style['fillColor'] = 'red'
            style['color'] = 'red'
            style['opacity'] = 0.0
        elif sts == "completed":
            style['fillColor'] = 'green'
            style['color'] = 'green'
            style['opacity'] = 0.0

        return style

    def _save_asset_thumbnail(self, idx: int, asset: str, mask_asset: str = None, nodata=0, threshold=None):
        import matplotlib.pyplot as plt

        img = self.zarr(asset)['tesseract'][idx, :, :, :]
        if mask_asset is not None:
            img *= self.ndarray(mask_asset)[0]

        img = np.squeeze(img, 0)
        if img.ndim == 3 and img.shape[0] != 3:
            print("couldn't display result, not compatible with visualization")
            return

        img, cmin, cmax = self._compute_image_overlay(img, nodata=nodata, threshold=threshold)

        fname = f'tmp-overlay-{asset}.png'
        plt.imsave(fname, img, cmap='magma', vmin=cmin, vmax=cmax)

        return fname

    def _compute_image_overlay(self, img: np.ndarray, nodata=0, threshold=None):
        from matplotlib.cm import magma

        if threshold is not None:
            img[img < threshold] = np.nanmin(img[img >= threshold])

        mu = np.nanmedian(img)
        std = np.nanstd(img)

        cmin = mu - std
        cmax = mu + std

        cmin = max(np.nanmin(img), cmin)
        cmax = min(np.nanmax(img), cmax)

        img = (img - cmin) / (cmax - cmin)

        if img.ndim == 2:
            nodata_idx = img == nodata
            img[nodata_idx] = np.nan
            img = magma(img)

            img *= 255
            img = img.astype(np.uint8)
            img = np.ascontiguousarray(img)

        return img, cmin, cmax

    def watch(self,
              basemap=None,
              display_last_result=False,
              asset=None,
              nodata=0,
              threshold=None,
              animate=False,
              mask_asset=None):
        """Monitor the tesseract job with the SeerAI widget.

        Will create a jupyter widget that will watch the progress of this tesseract job.
        """
        if basemap is None:
            basemap = ipyleaflet.basemaps.CartoDB.DarkMatter

        have_ipywidgets = True
        try:
            ipywidgets.VBox
        except ImportError:
            have_ipywidgets = False

        if not self.job_id:
            if have_ipywidgets:
                display.display(ipywidgets.HTML(
                    value='<h2 style="color: red;">No Job ID - submit job before watching</h2>'
                ))
                return
            raise ValueError("no job_id: has job been submitted?")

        self.status(return_quark_status=True)
        if not have_ipywidgets:
            return self.watch_terminal()

        widget, valid = self.widget(basemap)
        display.display(widget)
        if not valid:
            return

        keep_watching = True
        while keep_watching:
            self._update_widget()
            time.sleep(1)
            if self._n_completed == self._n_quarks:
                break

        if display_last_result and asset is not None:
            fname = self._save_asset_thumbnail(-1, asset, mask_asset, nodata, threshold=threshold)
            img_layer = ipyleaflet.ImageOverlay(
                url='files/'+os.path.split(os.getcwd())[-1]+f'/{fname}',
                bounds=self._bounds
            )
            self.map.add_layer(img_layer)

    def watch_terminal(self):
        with tqdm.tqdm(total=self._n_quarks) as progress:
            while True:
                state = self._state
                if state == "dry_run":
                    break
                progress.set_description(f"Job State: {self._state}")
                self.status()
                progress.update(self._n_completed)

                time.sleep(1)
                if self._n_completed == self._n_quarks:
                    break
        print(f"Job State: {self._state}")

    def _update_widget(self):
        quark_status = self.status(return_quark_status=True, return_quark_geoms=True)

        for k, status in quark_status['quark_status'].items():
            self.quark_geoms_lookup[k].properties['status'] = status

        feats = {
            'type': "FeatureCollection",
            'features': [f for _, f in self.quark_geoms_lookup.items()]
        }
        self._quark_layer.data = feats

        # set numerics
        self._prog.value = self._n_completed
        self._title.value = self._get_title()
        self._ratio.value = self._get_ratio()

    def _get_title(self):
        return f"<h2>Job ID: {self.alias} - {self._state}</h2>"

    def _get_ratio(self):
        return f"<h2>{self._n_completed} / {self._n_quarks}</h2>"

    def _calc_zoom_center(self):

        x_min = 0
        y_min = 1
        x_max = 2
        y_max = 3

        c = self._item['bbox']
        if self._bounds is None:
            self._bounds = [[c[y_min], c[x_min]], [c[y_max], c[x_max]]]
        center = ((c[y_max]+c[y_min]) / 2.0, (c[x_max] + c[x_min]) / 2.0)

        scale_x = (c[x_max] - c[x_min]) / 360
        scale_y = (c[y_max] - c[y_min]) / 180
        scale = max(scale_x, scale_y)

        if scale > 0:
            zoom = ceil(-np.log2(scale + 1e-9))
        else:
            zoom = 21

        zoom = max(0, zoom)
        zoom = min(21, zoom)
        return zoom, center, self._bounds
