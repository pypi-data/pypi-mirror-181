import json

import geopandas as gpd
import pandas as pd
from shapely import wkt


class GPDVector():
    gdf: gpd.GeoDataFrame

    def __init__(self, gdf: gpd.GeoDataFrame):
        self.gdf = gdf

    @classmethod
    def from_excel(cls, src, sheet_name='Sheet1', crs='epsg:4326') -> 'GPDVector':
        df = pd.read_excel(src)
        df['geometry'] = df['geometry'].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, crs=crs)
        return cls(gdf)

    @classmethod
    def from_shp(cls, src) -> 'GPDVector':
        gdf = gpd.read_file(src)
        return cls(gdf)

    @classmethod
    def from_df(cls, df, geom_col='geometry', crs='epsg:4326') -> 'GPDVector':
        gdf = gpd.GeoDataFrame(df, geometry=df[geom_col], crs=crs)
        return cls(gdf)

    @classmethod
    def from_gpkg(cls, src, layer) -> 'GPDVector':
        gdf = gpd.read_file(src, layer=layer)
        return cls(gdf)

    def to_gpkg(self, des, layer):
        self.gdf.to_file(des, layer=layer, driver="GPKG")

    def to_excel(self, des):
        self.gdf.to_excel(des)

    def get_srs(self) -> str:
        return self.gdf.crs.srs

    def get_crs(self):
        return self.gdf.crs

    def to_crs(self, srid):
        if str(self.gdf.crs) != f"epsg:{srid}":
            self.gdf.to_crs(epsg=srid, inplace=True)

    def inplace_result(self, gdf, inplace) -> 'GPDVector':
        if inplace:
            self.gdf = gdf
            return self
        else:
            return GPDVector(gdf)

    def extract_sub_data(self, col_name, col_val, inplace=True) -> 'GPDVector':
        if isinstance(col_val, list):
            res = []
            for v in col_val:
                res.append(self.gdf[self.gdf[col_name] == v])

            gdf = gpd.GeoDataFrame(pd.concat(res, ignore_index=True), crs=self.get_crs())
        else:
            gdf = self.gdf[self.gdf[col_name] == col_val]
        return self.inplace_result(gdf, inplace)

    def select_columns(self, cols, inplace=True):
        gdf = self.gdf[cols]
        return self.inplace_result(gdf, inplace)

    def add_area_col(self, unit='sq.km'):
        gdf = self.gdf.to_crs(epsg='3857') if self.gdf.crs.is_geographic else self.gdf
        self.gdf['area'] = round(gdf.geometry.area / (1000 * 1000), 3)

    def head(self, n=5):
        print(self.gdf.head(n=n))

    def tail(self, n=5):
        print(self.gdf.tail(n=n))

    def get_geometry(self, col_name, col_val):
        res = self.gdf[self.gdf[col_name] == col_val]['geometry']
        if not res.empty:
            return res.values[0]

    def get_gdf(self):
        return self.gdf

    def spatial_join(self, input_gdf: gpd.GeoDataFrame, predicate='intersects', how="inner") -> 'GPDVector':
        # inp, res = self.gdf.geometry.sindex.query_bulk(input_gdf.geometry, predicate=predicate)
        # res_df = pd.DataFrame({
        #     'self_index': res,
        #     'inp_index': inp
        # })
        # return res_df
        if str(input_gdf.crs) != str(self.get_crs()):
            input_gdf = input_gdf.to_crs(self.get_crs())
        join_result = self.gdf.sjoin(input_gdf, how="inner", predicate=predicate)
        return GPDVector(join_result)

    def to_goejson(self):
        geojson = json.loads(self.gdf.to_json())
        return geojson
