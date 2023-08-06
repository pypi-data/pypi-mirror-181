import logging
import os
import re
import traceback
from itertools import product

import geopandas as gpd
from typing import Union

import numpy as np
import pyproj
import rasterio
from affine import Affine
from fiona.crs import from_epsg
from rasterio import DatasetReader, MemoryFile, windows
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from rasterio.enums import Resampling
# from rasterio.session import AWSSession
from rasterio.features import shapes
from rasterio.mask import mask
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject

from shapely.geometry import Point, shape, box, Polygon
from shapely.ops import transform

from digitalarztools.io.file_io import FileIO
from digitalarztools.raster.indices import IndicesCalc
from digitalarztools.utils.da_logger import da_logger


class RioRaster:
    # src: str
    dataset: DatasetReader = None
    parent_img_name: str = None
    temp_dir: str = None

    def __init__(self, src: Union[str, DatasetReader], prj_path: str = None):
        self.set_dataset(src)
        if prj_path:
            self.add_crs_from_prj(prj_path)
        # self.temp_dir = os.path.join('temp', 'rio_raster')
        # if not os.path.exists(self.temp_dir):
        #     os.makedirs(self.temp_dir)

    def set_temp_folder(self, temp_dir: str):
        self.temp_dir = temp_dir

    def plot_data(self, band_nu: int = -1):
        # plt.imshow(data)
        # plt.colorbar()
        # plt.title('Overview - Band 4 {}'.format(thumbnail.shape))
        # plt.xlabel('Column #')
        # plt.ylabel('Row #')
        if band_nu == -1:
            show(self.dataset)
        else:
            show(self.dataset.read(1), transform=self.get_geo_transform())
        pass

    def set_dataset(self, src: Union[str, DatasetReader]):
        if isinstance(src, DatasetReader):
            self.dataset = src
        elif isinstance(src, str):
            if "s3://" in src:
                print("S3 not available")
                # self.dataset = S3Utils().get_rio_dataset(src)
            elif "/vsimem/" in src:
                with MemoryFile(src) as memfile:
                    self.dataset = memfile.open()
            else:
                if os.path.exists(src):
                    self.dataset = rasterio.open(src, mode='r+')

    def get_dataset(self) -> DatasetReader:
        return self.dataset

    def get_meta(self):
        return self.dataset.meta

    def get_dtype(self):
        return self.dataset.meta['dtype']

    def get_nodata_value(self):
        return self.dataset.meta['nodata']

    def get_overviews(self, num):
        oviews = self.dataset.overviews(1)  # list of overviews from biggest to smallest
        return oviews

    def get_profile(self):
        return self.dataset.profile

    def get_file_name(self) -> (str, str):
        if self.dataset.files and len(self.dataset.files) > 0:
            file_name = str(self.dataset.files[0])
            dir_name = os.path.dirname(file_name)
            base_name = os.path.basename(file_name)
            return dir_name, base_name

    @classmethod
    def separate_file_path_name(cls, file_path_name: str):
        file_dir = os.path.dirname(file_path_name)
        file_name = os.path.basename(file_path_name)
        return file_dir, file_name

    @classmethod
    def get_file_name_extension(cls, file_name: str) -> (str, str):
        split = file_name.split(".")
        if len(split) == 2:
            return split[0], split[1]
        return file_name, None

    def get_file_extension(self):
        try:
            dir, name = self.separate_file_path_name(self.get_file_name())
            name, ext = self.get_file_name_extension(name)
            return ext
        except Exception as e:
            traceback.print_exc()

    def get_bounds(self) -> BoundingBox:
        return self.dataset.bounds

    def get_envelope(self) -> Polygon:
        return box(*self.get_bounds())

    def get_envelope_gdf(self) -> gpd.GeoDataFrame:
        srid = self.get_raster_srid()
        return gpd.GeoDataFrame({'geometry': self.get_envelope()}, index=[0], crs=from_epsg(srid))

    def get_raster_extent(self) -> list:
        bounds = self.dataset.bounds
        return [bounds.left, bounds.bottom, bounds.right, bounds.top]

    def get_raster_extent_in_4326(self) -> list:
        bounds = self.dataset.bounds
        point_lb = Point(bounds.left, bounds.bottom)
        point_rt = Point(bounds.right, bounds.top)
        point_lb = self.transform_geometry(point_lb)
        point_rt = self.transform_geometry(point_rt)
        return [point_lb.x, point_lb.y, point_rt.x, point_rt.y]

    def get_raster_srid(self) -> int:
        try:
            # epsg_code = int(self.dataset.crs.data['init'][5:])
            profile = self.get_profile()
            wkt = str(profile['crs'])
            if ':' in wkt:
                return int(str(profile['crs']).split(":")[-1])
            else:
                crs = pyproj.CRS.from_wkt(wkt)
                return crs.to_epsg()
        except Exception as e:
            traceback.print_exc()
            return 0

    def set_crs(self, crs: pyproj.CRS):
        crs = rasterio.crs.CRS.from_wkt(crs.to_wkt())
        self.dataset.crs = crs

    def get_crs(self):
        return self.dataset.crs

    def get_width(self):
        return self.dataset.width

    def get_height(self):
        return self.dataset.height

    def get_pyproj_crs(self) -> pyproj.CRS:
        try:
            # profile = self.get_profile()
            # epsg_code = str(profile['crs'])
            return pyproj.CRS.from_wkt(self.dataset.crs.to_wkt())
        except Exception as e:
            traceback.print_exc()
            return None

    def transform_geometry(self, geometry, to_srid=4326):
        from_crs = self.get_pyproj_crs()
        if from_crs and from_crs.to_epsg() != to_srid:
            to_crs = pyproj.CRS(f'EPSG:{to_srid}')
            project = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform
            return transform(project, geometry)
        return geometry

    def get_data_shape(self):
        data = self.get_data_array()
        if len(data.shape) == 2:
            band = 1
            row, column = data.shape
        elif len(data.shape) == 3:
            band, row, column = data.shape
        return band, row, column

    def get_data_array(self, band=None, convert_no_data_2_nan=False) -> np.ndarray:
        if band:
            data_arr = self.dataset.read(band)
        else:
            data_arr = self.dataset.read()
        if convert_no_data_2_nan:
            data_arr = data_arr.astype(np.float)
            data_arr[data_arr == self.dataset.nodata] = np.nan
        return data_arr

    def save_to_file(self, img_des: str, data: np.ndarray = None, crs: CRS = None, transform: Affine = None,
                     nodata_value=None):
        dir_name = os.path.dirname(img_des)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        def create_new_raster(arr: np.ndarray):
            if len(arr.shape) == 2:
                bands = 1
                rows, cols = arr.shape
            else:
                bands, rows, cols = arr.shape
            dataset = rasterio.open(img_des, 'w',
                                    driver='GTiff',
                                    height=rows,
                                    width=cols,
                                    count=bands,
                                    dtype=str(arr.dtype),
                                    crs=crs if crs else self.dataset.crs,
                                    transform=transform if transform else self.dataset.transform,
                                    nodata=nodata_value if nodata_value else self.get_nodata_value()
                                    )
            for i in range(bands):
                d = arr if len(arr.shape) == 2 else arr[i]
                dataset.write(d, i + 1)
            dataset.close()

        if data is None:
            data = self.get_data_array()

        # if "s3://" in img_des:
        #     session = rasterio.Env(AWSSession(S3Utils().get_session()))
        #     with session:
        #         create_new_raster(data)
        #
        # else:
        create_new_raster(data)

    @staticmethod
    def raster_from_array(img_arr: np.ndarray, crs: Union[str, CRS],
                          transform: Affine, nodata_value=None) -> 'RioRaster':
        """

        :param img_arr:
        :param crs: pyproj.CRS or wkt
        :param transform:
            Affine consist of a, b, c, d, e, f format
        :param nodata_value:
        :return:
        """
        memfile = MemoryFile()
        if len(img_arr.shape) == 2:
            bands = 1
            rows, cols = img_arr.shape
        else:
            bands, rows, cols = img_arr.shape
        dataset = memfile.open(driver='GTiff',
                               height=rows,
                               width=cols,
                               count=bands,
                               dtype=str(img_arr.dtype),
                               crs=crs,
                               transform=transform,
                               nodata=nodata_value
                               )
        for i in range(bands):
            d = img_arr if len(img_arr.shape) == 2 else img_arr[i, :, :]
            dataset.write(d, i + 1)
        dataset.close()

        dataset = memfile.open()  # Reopen as DatasetReader
        # dir_name, file_name = self.get_file_name()
        new_raster = RioRaster(dataset)

        return new_raster

    def add_crs_from_prj(self, prj_file):
        crs = FileIO.read_prj_file(prj_file)
        self.dataset.crs = CRS.from_wkt(crs.to_wkt())

    def get_driver(self):
        return self.get_profile().data['driver']

    def get_img_resolution(self) -> tuple:
        cols = self.get_profile().data['width']
        rows = self.get_profile().data['height']
        return rows, cols

    def get_spatial_resoultion(self) -> tuple:
        bounds = self.get_bounds()
        s_width = bounds.right - bounds.left
        i_width = self.get_width()
        s_height = bounds.top - bounds.bottom
        i_height = self.get_height()
        return (s_width / i_width, s_height / i_height)

    def get_radiometric_resolution(self):
        s = self.get_profile()['dtype']
        m = re.search(r'\d+$', s)
        return int(m.group()) if m else None

    def get_spectral_resolution(self):
        return self.get_profile().data['count']

    # def get_no_of_bands(self):
    #     return self.dataset.count

    def get_geo_transform(self) -> Affine:
        return self.get_profile().data['transform']

    def is_image_crs_same(self, raster2: 'RioRaster') -> bool:
        crs1 = self.get_crs()
        crs2 = raster2.get_crs()
        return str(crs1) == str(crs2)

    def is_image_resolution_same(self, raster2: 'RioRaster') -> bool:
        res1 = self.get_img_resolution()
        res2 = raster2.get_img_resolution()
        return res1 == res2

    def is_image_extent_same(self, raster2: 'RioRaster'):
        E1 = np.array(self.get_raster_extent())
        E2 = np.array(raster2.get_raster_extent())
        return (E1 == E2).all()

    def create_ndwi_data(self, green, nir, output_path: str = None):
        nir_data = self.get_data_array(nir)
        green_data = self.get_data_array(green)
        ndwi = IndicesCalc.NDWIndices(green_data, nir_data)
        ndwi = IndicesCalc.normalize(ndwi)
        if output_path:
            self.save_to_file(output_path, ndwi.astype(rasterio.int8))
        return ndwi

    def create_ndvi_data(self, red_band: int, nir_band: int, output_path: str = None):
        nir_data = self.get_data_array(nir_band)
        red_data = self.get_data_array(red_band)
        ndvi = IndicesCalc.NDVIndices(nir_data, red_data)
        ndvi = IndicesCalc.normalize(ndvi)
        if output_path:
            self.save_to_file(output_path, ndvi.astype(rasterio.int8))
        return ndvi
        # with rasterio.open('Data_06/RASTER/NDVI/NDVI.tif', 'w', **meta_ndvi) as dst:
        #     dst.write_band(1, ndvi.astype(rasterio.float32))

    def raster_2_vector(self, band: Union[int, np.ndarray]) -> gpd.GeoDataFrame:
        geoms = []
        file_path, file_name = self.get_file_name()
        if isinstance(band, np.ndarray):
            band_data = band
        else:
            band_data = self.get_data_array(band)
        c_ids = []
        for vec in shapes(band_data, transform=self.get_geo_transform()):
            geoms.append(shape(vec[0]))
            c_ids.append(vec[1])
        # ids = np.arange(len(geoms))
        gdf = gpd.GeoDataFrame({'geometry': geoms,
                                'class_id': np.array(c_ids).astype('uint16'),
                                'grid': file_name.split('.')[0]
                                })
        gdf.crs = self.get_pyproj_crs()
        return gdf

    def get_tiles(self, width=64, height=64) -> 'RioRaster':
        rows, cols = self.get_img_resolution()
        offsets = product(range(0, cols, width), range(0, rows, height))
        big_window = windows.Window(col_off=0, row_off=0, width=cols, height=rows)
        for col_off, row_off in offsets:
            window = windows.Window(col_off=col_off, row_off=row_off,
                                    width=width, height=height).intersection(big_window)
            transform = windows.transform(window, self.get_geo_transform())
            tile = self.dataset.read(window=window)
            tile_raster = self.raster_from_array(tile, crs=self.get_crs(), transform=transform,
                                                 nodata_value=self.get_nodata_value())
            # print(f"working on tile of {self.get_file_name()[1]} at {window}")
            yield tile_raster, col_off, row_off

    def get_all_tiles(self):
        tiles = []
        tile_no = 0
        tile_raster: RioRaster
        if self.temp_dir:
            for tile_raster in self.get_titles(width=500, height=500):
                tile_no += 1
                file_name = self.get_file_name()[1].split('.')[0]
                tile_name = f"{self.temp_dir}/tiles/{file_name}_{tile_no}.tif"
                tile_raster.save_to_file(tile_name)
                tiles.append(tile_name)
            return tiles
        else:
            da_logger.critical("Please set temp folder path first using set_temp_folder")

    @staticmethod
    def reverse_band_row_col(data: np.ndarray):
        return np.moveaxis(data, 0, 2)

    def save_temp_file(self, postfix: str):
        if self.temp_dir:
            img_name = self.get_file_name().split('.')[-2]
            img_des = os.path.join(self.temp_dir, f"{img_name}_{postfix}.tif")
            print(img_des)
            self.save_to_file(img_des)
        else:
            da_logger.critical("Please set temp folder path first using set_temp_folder")

    def resample_raster(self, width, height):
        bands = self.dataset.count
        data = self.dataset.read(
            out_shape=(
                bands,
                int(height),
                int(width)
            ),
            resampling=Resampling.bilinear
        )
        transform = self.dataset.transform * self.dataset.transform.scale(
            (self.dataset.width / data.shape[-1]),
            (self.dataset.height / data.shape[-2])
        )
        kwargs = self.dataset.meta.copy()
        kwargs.update({
            'transform': transform,
            'width': data.shape[-1],
            'height': data.shape[-2]
        })
        memfile = MemoryFile()
        dst = memfile.open(**kwargs)
        for i in range(bands):
            d = data if len(data.shape) == 2 else data[i, :, :]
            dst.write(d, i + 1)
        dst.close()
        self.dataset = memfile.open()  # Reopen as DatasetReader

    def reproject_raster(self, dst_pyproj_crs: pyproj.CRS = None, width=None, height=None):
        src = self.dataset
        dst_crs = rasterio.crs.CRS.from_wkt(dst_pyproj_crs.to_wkt())
        dst_crs = self.get_crs() if dst_crs is None else dst_crs
        width = self.get_width() if width is None else width
        height = self.get_height() if height is None else height
        transform, width, height = calculate_default_transform(self.get_crs(), dst_crs, width,
                                                               height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        memfile = MemoryFile()
        dst = memfile.open(**kwargs)
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)
        dst.close()
        self.dataset = memfile.open()

    def pad_raster(self, des_bounds, save_temp_file: bool = False):
        bands = self.get_spectral_resolution()
        # ulx = gt[0] - gt[1] * npad
        # uly = gt[3] - gt[5] * npad
        aff: Affine = self.get_geo_transform()
        row_min, col_min = rasterio.transform.rowcol(aff, des_bounds[0], des_bounds[3])
        row_max, col_max = rasterio.transform.rowcol(aff, des_bounds[2], des_bounds[1])
        height = row_max - row_min
        width = col_max - col_min
        window = windows.Window(col_off=col_min, row_off=row_min,
                                width=width, height=height)  # .intersection(big_window)
        transform = windows.transform(window, self.get_geo_transform())
        kwargs = self.dataset.meta.copy()
        kwargs.update({
            'crs': self.get_crs(),
            'transform': transform,
            'width': width,
            'height': height
        })
        memfile = MemoryFile()
        dst = memfile.open(**kwargs)
        # for i in range(bands):
        #     # tile = self.dataset.read()
        data = self.dataset.read(window=window, boundless=True, fill_value=self.dataset.nodata)
        dst.write(data)
        dst.close()
        self.dataset = memfile.open()
        if save_temp_file:
            self.save_temp_file('padded')

    def reclassify_raster(self, thresholds, band=1, nodata=0):
        """
        :param thresholds:
            example:  {
                    "water": (('lt', 0.015), 4),
                    "built-up": ((0.015, 0.02), 1),
                    "barren": ((0.07, 0.27), 2),
                    "vegetation": (('gt', 0.27), 3)
                }
        :param band:
            band no
        :return:
        """
        img_arr = self.get_data_array(band)
        res = np.empty(img_arr.shape)
        res[:] = nodata
        for key in thresholds:
            if thresholds[key][0][0] == 'lt':
                res = np.where(img_arr <= thresholds[key][0][1], thresholds[key][1], res)
            elif thresholds[key][0][0] == 'gt':
                res = np.where(img_arr >= thresholds[key][0][1], thresholds[key][1], res)
            else:
                con = np.logical_and(img_arr >= thresholds[key][0][0], img_arr <= thresholds[key][0][1])
                res = np.where(con, thresholds[key][1], res)
        return res.astype(np.uint8)

    def clip_raster(self, aoi: Union[Polygon, gpd.GeoDataFrame], crs: CRS) -> 'RioRaster':
        """
        :param aoi: shapely polygon geometry
        :param crs: pyproj.CRS
        :return: RioRaster
        """
        if str(crs).lower() != str(self.get_crs()).lower():
            geo = aoi.to_crs(self.get_crs())
        else:
            geo = aoi

        if isinstance(aoi, Polygon):
            geo = gpd.GeoDataFrame({'geometry': aoi}, index=[0], crs=crs)

        out_meta = self.dataset.meta.copy()

        def getFeatures(gdf):
            """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
            import json
            return [json.loads(gdf.to_json())['features'][0]['geometry']]

        coords = getFeatures(geo)
        out_img, out_transform = mask(dataset=self.dataset, shapes=coords, crop=True, pad=True)
        out_meta.update({"driver": "GTiff",
                         "height": out_img.shape[1],
                         "width": out_img.shape[2],
                         "transform": out_transform,
                         "crs": self.dataset.crs})
        dataset = self.rio_dataset_from_array(out_img, out_meta)
        return RioRaster(dataset)

    def make_coincident_with(self, img_raster: 'RioRaster', save_temp_file: bool = False):

        # if img_raster.get_raster_srid() != self.get_raster_srid():
        if not self.is_image_crs_same(img_raster):
            self.reproject_raster(img_raster.get_crs())
        des_bbox = box(*img_raster.get_bounds())
        src_bbox = box(*self.get_bounds())
        if not des_bbox.equals(src_bbox):
            if src_bbox.within(des_bbox):
                self.pad_raster(img_raster.get_bounds(), save_temp_file)
            else:
                srid = self.get_raster_srid()
                geo = gpd.GeoDataFrame({'geometry': des_bbox}, index=[0], crs=from_epsg(srid))
                self.clip_raster(geo, save_temp_file)
        # if img_raster.get_height() != self.get_height() or img_raster.get_width() != self.get_width():
        if not self.is_image_resolution_same(img_raster):
            self.resample_raster(img_raster.get_width(), img_raster.get_height())

    @classmethod
    def rio_dataset_from_array(cls, data: np.ndarray, meta) -> DatasetReader:

        bands = 1 if len(data.shape) == 2 else data.shape[0]
        memfile = MemoryFile()
        dst = memfile.open(**meta)
        for i in range(bands):
            d = data if len(data.shape) == 2 else data[i, :, :]
            dst.write(d, i + 1)
        dst.close()
        dataset = memfile.open()  # Reopen as DatasetReader
        return dataset
