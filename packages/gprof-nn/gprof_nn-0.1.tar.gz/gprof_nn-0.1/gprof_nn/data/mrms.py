"""
==================
gprof_nn.data.mrms
==================

Interface class to read GPROF MRMS match ups used over snow surfaces.
"""
import gzip
from pathlib import Path

import numpy as np
import xarray as xr
import pandas as pd
from pyresample import geometry, kd_tree
from pykdtree.kdtree import KDTree
from scipy.signal import convolve

from gprof_nn import sensors
from gprof_nn.coordinates import latlon_to_ecef
from gprof_nn.data.validation import unify_grid, calculate_angles
from gprof_nn.utils import calculate_smoothing_kernel


class MRMSMatchFile:
    """
    Class to read GMI-MRMS match up files.

    Attributes:
        data: Numpy structured array holding raw MRMS match-up data.
        n_obs: The number of observations in the file.
        scan_time: Array holding the scan times for each match up.
        year: The year from which the observations stem.
        month: The month from which the observations stem.
    """

    file_pattern = "*_MRMS2{sensor}_*.bin.gz"

    @classmethod
    def find_files(cls, path, sensor=sensors.GMI):
        """
        Generator providing access to all files that match the naming scheme
        for GMI-MRMS match file in a give folder.

        Args:
            path: Path to the directory containing the GMI-MRMS matchup files.

        Return:
            Generator object returning the paths of all GMI-MRMS match up
            files in the given directory.
        """
        path = Path(path)
        return list(path.glob(cls.file_pattern.format(sensor=sensor.name)))

    def __init__(self, filename, sensor=None):
        """
        Reads gzipped matchup file.

        Args:
            filename: The name of the file to read.
        """
        filename = Path(filename)
        if sensor is None:
            if "GMI" in filename.name:
                sensor = sensors.GMI
            elif "MHS" in filename.name:
                sensor = sensors.MHS
            elif "SSMIS" in filename.name:
                sensor = sensors.SSMIS
            elif "AMSR2" in filename.name:
                sensor = sensors.AMSR2
            else:
                raise ValueError(
                    "Could not infer sensor from filename. Consider passing "
                    "the sensor argument explicitly."
                )
        self.sensor = sensor

        with open(filename, "rb") as source:
            buffer = gzip.decompress(source.read())
        self.data = np.frombuffer(buffer, sensor.mrms_file_record)
        self.n_obs = self.data.size

        self.scan_time = np.zeros(self.n_obs, dtype="datetime64[ns]")
        for i in range(self.n_obs):
            dates = self.data["scan_time"]
            year = dates[i, 0]
            month = dates[i, 1]
            day = dates[i, 2]
            hour = dates[i, 3]
            minute = dates[i, 4]
            self.scan_time[i] = np.datetime64(
                f"{year:04}-{month:02}-{day:02}" f"T{hour:02}:{minute:02}:00"
            )

        name = Path(filename).name
        self.year = int(name[:2])
        self.month = int(name[2:4])

    def to_xarray_dataset(self, day=None):
        """
        Load data into xarray.Dataset.

        Args:
            day: If given only the data for a given day of the month will
                be included in the dataset.

        Return:
            xarray.Dataset containing the MRMS match-up data.
        """
        if day is not None:
            indices = self.data["scan_time"][:, 2] == day
            if not np.any(indices):
                return xr.Dataset()

        else:
            indices = np.arange(self.data.size)
        data = self.data[indices]
        dims = ("samples",)
        dataset = {}
        for k in self.sensor.mrms_file_record.names:
            if k == "brightness_temperatures":
                ds = dims + ("channels",)
            elif k == "scan_time":
                dataset[k] = (("samples",), self.scan_time[indices])
                continue
            else:
                ds = dims
            dataset[k] = (ds, data[k])

        dataset = xr.Dataset(dataset)
        if dataset.channels.size < self.sensor.n_chans:
            dataset = dataset[{"channels": self.sensor.gmi_channels}]

        return dataset

    def match_targets(self, input_data):
        """
        Match available retrieval targets from MRMS data to points in
        xarray dataset.

        Args:
            input_data: xarray dataset containing the input data from
                the preprocessor.
        Return:
            The input dataset but with the surface_precip field added.
        """
        start_time = input_data["scan_time"].data[0]
        end_time = input_data["scan_time"].data[-1]
        indices = (self.scan_time >= start_time) * (self.scan_time < end_time)

        data = self.data[indices]

        n_scans = input_data.scans.size
        n_pixels = input_data.pixels.size

        if indices.sum() <= 0:
            surface_precip = np.zeros((n_scans, n_pixels))
            surface_precip[:] = np.nan
            input_data["surface_precip"] = (("scans", "pixels"), surface_precip)

            input_data["convective_precip"] = (("scans", "pixels"), surface_precip)
            return input_data

        lats_1c = input_data["latitude"].data.reshape(-1, 1)
        lons_1c = input_data["longitude"].data.reshape(-1, 1)
        coords_1c = latlon_to_ecef(lons_1c, lats_1c)
        coords_1c = np.concatenate(coords_1c, axis=1)

        lats = data["latitude"].reshape(-1, 1)
        lons = data["longitude"].reshape(-1, 1)
        coords_sim = latlon_to_ecef(lons, lats)
        coords_sim = np.concatenate(coords_sim, 1)

        kdtree = KDTree(coords_1c)
        dists, indices = kdtree.query(coords_sim)

        matched = np.zeros(n_scans * n_pixels)
        matched[:] = np.nan
        matched[indices] = data["surface_precip"]

        mrms_ratios = get_mrms_ratios()
        ratios = mrms_ratios.interp(
            latitude=xr.DataArray(lats.ravel(), dims="samples"),
            longitude=xr.DataArray(lons.ravel(), dims="samples"),
        )
        corrected = data["surface_precip"] - data["snow"] + data["snow"] * ratios
        corrected[ratios == 1.0] = np.nan

        matched[indices] = corrected
        matched[indices][dists > 15e3] = np.nan
        matched = matched.reshape((n_scans, n_pixels))
        input_data["surface_precip"] = (("scans", "pixels"), matched)

        matched = np.zeros(n_scans * n_pixels)
        matched[:] = np.nan
        matched[indices] = data["convective_rain"]
        matched[indices][dists > 15e3] = np.nan
        matched = matched.reshape((n_scans, n_pixels))
        input_data["convective_precip"] = (("scans", "pixels"), matched)

        if "snow3" in data.dtype.names:
            for var in ["snow", "snow3", "snow4"]:
                matched = np.zeros(n_scans * n_pixels)
                matched[:] = np.nan
                matched[indices] = data[var]
                matched[indices][dists > 15e3] = np.nan
                matched = matched.reshape((n_scans, n_pixels))
                input_data[var] = (("scans", "pixels"), matched)

        return input_data


###############################################################################
# MRMS / snodas correction factors
###############################################################################

_RATIO_FILE = (
    "/qdata1/pbrown/dbaseV7/mrms_snow_scale_factors/"
    "201710-201805_10km_snodas_mrms_ratio_scale.asc."
    "bin"
)

_MRMS_RATIOS = None


def has_snowdas_ratios():
    """
    Simple test function to determine whether snowdas ratio files are
    present on system.
    """
    return Path(_RATIO_FILE).exists()


def get_mrms_ratios():
    """
    Cached loading of the MRMS correction factors into an xarray
    data array.

    Return:
        xrray.Dataarray containing the MRMS/SNODAS ratios used to correct
        MRMS snow.
    """
    global _MRMS_RATIOS
    if _MRMS_RATIOS is None:
        with open(_RATIO_FILE, "rb") as file:
            buffer = file.read()
            lon_ll = -129.994995117188
            d_lon = 0.009998570017
            n_lon = 7000
            lons = lon_ll + d_lon * np.arange(n_lon)

            lat_ll = 20.005001068115
            d_lat = 0.009997142266
            n_lat = 3500
            lats = lat_ll + d_lat * np.arange(n_lat)

            offset = 2 * 2 + 4 * 8 + 4
            array = np.frombuffer(
                buffer, dtype="f4", offset=offset, count=n_lon * n_lat
            )
            ratios = array.reshape((n_lat, n_lon)).copy()
            ratios[ratios < 0] = np.nan

            _MRMS_RATIOS = xr.DataArray(
                data=ratios,
                dims=["latitude", "longitude"],
                coords={"latitude": lats, "longitude": lons},
            ).fillna(1.0)
    return _MRMS_RATIOS


def resample_to_swath(mrms_data, sensor, l1c_data):
    """
    Resample MRMS data to uniform grid along satellite swath.

    Args:
        mrms_data: xarray.Dataset containing the MRMS data.
        sensor: Sensor object representing the sensor from which the L1C data
            stems.
        l1c_data: The L1C data matching the MRMS measurements.
    """
    from gprof_nn.validation import smooth_reference_field

    mrms_data = mrms_data.copy(deep=True)
    lons = mrms_data.longitude.data
    lons[lons > 180] -= 360.0

    lats = l1c_data.latitude.data
    lons = l1c_data.longitude.data

    # Find scans over MRMS domain.
    lat_min = mrms_data.latitude.data.min()
    lat_max = mrms_data.latitude.data.max()
    lon_min = mrms_data.longitude.data.min()
    lon_max = mrms_data.longitude.data.max()

    indices = np.where(
        np.any(
            ((lats >= lat_min) *
             (lats <= lat_max) *
             (lons >= lon_min) *
             (lons <= lon_max)),
            axis=-1
        )
    )[0]
    scan_start = indices[0]
    scan_end = indices[-1]

    l1c_data = l1c_data[{"scans": slice(scan_start, scan_end)}]
    lats = l1c_data.latitude.data
    lons = l1c_data.longitude.data

    # Restrict MRMS to swath domain to speed up convolution
    lat_min = lats.min() - 0.1
    lat_max = lats.max() + 0.1
    lon_min = lons.min() - 0.1
    lon_max = lons.max() + 0.1
    lon_start, lon_end = np.where(
        (mrms_data.longitude.data > lon_min) *
        (mrms_data.longitude.data < lon_max)
    )[0][[0, -1]]
    lat_start, lat_end = np.where(
        (mrms_data.latitude.data > lat_min) *
        (mrms_data.latitude.data < lat_max)
    )[0][[0, -1]]
    mrms_data = mrms_data[{
        "longitude": slice(lon_start, lon_end),
        "latitude": slice(lat_start, lat_end)
    }]

    # Calculate 5km x 5km grid.
    lats_5, lons_5 = unify_grid(lats, lons, sensor)
    lats_5 = xr.DataArray(data=lats_5, dims=["along_track", "across_track"])
    lons_5 = xr.DataArray(data=lons_5, dims=["along_track", "across_track"])

    # Calculate antenna angle
    if isinstance(sensor, sensors.ConicalScanner):
        angles = calculate_angles(l1c_data)
    elif isinstance(sensor, sensors.CrossTrackScanner):
        angles = l1c_data.incidence_angle.data
    else:
        raise ValueError(
            "Sensor object must be either a 'ConicalScanner' or "
            "a 'CrossTrackScanner'."
        )

    # Define swaths for resampling.
    swath = geometry.SwathDefinition(lats=lats, lons=lons)
    swath_5 = geometry.SwathDefinition(lats=lats_5, lons=lons_5)
    angles = kd_tree.resample_nearest(
        swath, angles, swath_5, radius_of_influence=20e3
    )

    results = xr.Dataset()
    results["latitude"] = lats_5
    results["longitude"] = lons_5

    if "precip_rate" in mrms_data.variables:
        # Smooth and interpolate surface precip
        surface_precip = mrms_data.precip_rate.copy()
        surface_precip.data[surface_precip.data < 0] = np.nan
        k = calculate_smoothing_kernel(5, 5, 2, 2)
        k /= k.sum()

        sp = np.nan_to_num(surface_precip.data.copy())
        counts = np.isfinite(surface_precip.data).astype(np.float32)

        # Use direct method to avoid negative values in results.
        sp_mean = convolve(sp, k, mode="same", method="direct")
        sp_cts = convolve(counts, k, mode="same", method="direct")
        sp = sp_mean / sp_cts
        # Set pixel with too few valid neighboring pixels to nan.
        sp[sp_cts < 1e-1] = np.nan
        surface_precip.data = sp

        surface_precip = surface_precip.interp(
            latitude=lats_5,
            longitude=lons_5,
            method="nearest",
            kwargs={"fill_value": np.nan}
        )
        results["surface_precip"] = (("along_track", "across_track"), surface_precip.data)
        surface_precip_avg = smooth_reference_field(
            sensor,
            surface_precip.data,
            angles,
            steps=11,
            resolution=5
        )
        results["surface_precip_avg"] = (
            ("along_track", "across_track"),
            surface_precip_avg
        )

    if "radar_quality_index" in mrms_data.variables:
        rqi = mrms_data.radar_quality_index.interp(
            latitude=lats_5, longitude=lons_5, method="nearest",
            kwargs={"fill_value": -1}
        )
        results["radar_quality_index"] = (
            ("along_track", "across_track"),
            rqi.data
        )

    results.attrs["sensor"] = sensor.sensor_name
    results.attrs["platform"] = sensor.platform.name

    # Remove empty scan lines.
    if "surface_precip" in results.variables:
        has_data = np.any(np.isfinite(results.surface_precip.data), -1)
    else:
        has_data = np.any(np.isfinite(results.radar_quality_index.data), -1)

    indices = np.where(has_data)[0]
    if len(indices) == 0:
        raise ValueError(
            "No valid precipitation pixels in overpass."
            )
    along_track_start = indices.min()
    along_track_end = indices.max()
    results = results[{
        "along_track": slice(along_track_start, along_track_end)
    }]
    return results
