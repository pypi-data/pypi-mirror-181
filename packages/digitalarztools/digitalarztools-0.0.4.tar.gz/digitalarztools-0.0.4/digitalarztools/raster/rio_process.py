import os
import geopandas as gpd
from pathlib import Path

import numpy as np
from rasterio import DatasetReader
from rasterio.merge import merge
from shapely.geometry import box

from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.feature_collection import GEEFeatureCollection
from digitalarztools.pipelines.gee.core.region import GEERegion
from digitalarztools.raster.rio_raster import RioRaster
from digitalarztools.utils.date_utils import DateUtils
from digitalarztools.vector.gpd_vector import GPDVector


class RioProcess:
    def __init__(self):
        pass

    @staticmethod
    def mosaic_images(img_folder: str) -> RioRaster:
        ds_files: [DatasetReader]
        path = Path(img_folder)
        # test = [str(p) for p in path.iterdir() if p.suffix == ".tif"]
        ds_files = [RioRaster(str(p)).get_dataset() for p in path.iterdir() if p.suffix == ".tif"]
        mosaic, out_trans = merge(ds_files)
        crs = ds_files[0].crs
        raster = RioRaster.raster_from_array(mosaic, crs=crs, transform=out_trans)
        return raster

    @staticmethod
    def classify_ndwi(rio_raster, band=8) -> np.ndarray:
        classes = {
            "vegetation": (('lt', 0.1), 3),
            "built-up": ((-0.1, 0.4), 1),
            "water": (('gt', 0.4), 4),
        }
        img_arr = rio_raster.get_data_array(band)
        res = rio_raster.reclassify_raster(img_arr, classes)
        return res.astype(np.uint8)

    # @staticmethod
    # def classify_based_on_ranges(img_arr: np.ndarray, classes: dict):
    #     res = np.empty(img_arr.shape)
    #     res[:] = np.NaN
    #     for key in classes:
    #         if classes[key][0][0] == 'lt':
    #             res = np.where(img_arr <= classes[key][0][1], classes[key][1], res)
    #         elif classes[key][0][0] == 'gt':
    #             res = np.where(img_arr >= classes[key][0][1], classes[key][1], res)
    #         else:
    #             con = np.logical_and(img_arr >= classes[key][0][0], img_arr <= classes[key][0][1])
    #             res = np.where(con, classes[key][1], res)
    #     return res

    @staticmethod
    def classify_ndwi(rio_raster: RioRaster, band=1) -> np.ndarray:
        classes = {
            "vegetation": (('lt', 0.1), 3),
            "built-up": ((-0.1, 0.4), 1),
            "water": (('gt', 0.4), 4),
        }
        img_arr = rio_raster.get_data_array(band)
        res = rio_raster.reclassify_raster(img_arr, classes)
        return res.astype(np.uint8)

    @staticmethod
    def classify_ndvi(rio_raster: RioRaster, band=1) -> np.ndarray:
        classes = {
            "water": (('lt', 0.015), 4),
            "built-up": ((0.015, 0.02), 1),
            "barren": ((0.07, 0.27), 2),
            "vegetation": (('gt', 0.27), 3)
        }
        print("no of bands", rio_raster.get_spectral_resolution())
        img_arr = rio_raster.get_data_array(band)
        res = rio_raster.reclassify_raster(img_arr, classes)
        return res.astype(np.uint8)

    @classmethod
    def combine_indices(cls, rio_raster):
        # values = np.unique(pc_classification)
        # for val in values:
        ndvi_classification = cls.classify_ndvi(rio_raster,7)
        ndwi_classification = cls.classify_ndwi(rio_raster,8)
        x = np.where(ndwi_classification == 1, ndwi_classification, ndvi_classification)
        x = np.where(ndwi_classification == 4, ndwi_classification, x)
        return x

    @classmethod
    def split_2_tiles(cls, raster: RioRaster, des_path: str, tile_width, tile_height, des_crs=None):
        FileIO.mkdirs(des_path)
        tile: RioRaster
        # tile_width, tile_height = 5000, 5000
        # nodata_value = self.raster.get_nodata_value()
        for tile, col_off, row_off in raster.get_tiles(tile_width, tile_height):
            if des_crs:
                tile.reproject_raster(des_crs)
            des_tile = os.path.join(des_path, f'tile_{int(col_off / tile_width)}_{int(row_off / tile_height)}.tif')
            tile.save_to_file(des_tile)
            print(f"saved at {des_tile}")
        cls.generate_index_map(des_path)

    @staticmethod
    def generate_index_map(tile_path):
        crs = None
        envelopes, col_index, row_index, file_name = [], [], [], []
        file_list = FileIO.get_files_list_in_folder(tile_path, ext='tif')
        for fp in file_list:
            raster = RioRaster(fp)
            if not crs:
                crs = raster.get_crs()
            e = box(*raster.get_raster_extent())
            envelopes.append(e)
            name_parts = FileIO.get_file_name_ext(fp)[0].split("_")
            col_index.append(name_parts[1])
            row_index.append(name_parts[1])
            file_name.append(os.path.basename(fp))
        gdf = gpd.GeoDataFrame({"file_name": file_name, "row_index": row_index, "col_index": col_index},
                               geometry=envelopes, crs=crs)
        gdp_vector = GPDVector(gdf)
        index_des = f"{tile_path}/index_map.gpkg"
        gdp_vector.to_gpkg(index_des, layer="index_map")
        print(f"saved at {index_des}")

    @staticmethod
    def min_max_stretch(raster: RioRaster, band:tuple) -> np.ndarray:
        """
        adjust only for single band like (1,) needd to update for more than one band
        :param raster:
        :param band:
        :return:
        """
        data = raster.get_data_array(band=band)
        data = data.astype(np.float32)
        data[data == raster.get_nodata_value()] = np.nan
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        data = (data - min_val) / (max_val - min_val) * 255
        data = data.astype(np.uint8)
        return data