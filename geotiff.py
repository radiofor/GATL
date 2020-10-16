# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
import time
import numpy as np
import imageio
import rasterio
import pandas as pd
import geopandas as gpd
from shapely import geometry as shapely_geom
import fileman
from geometry import Polygon as gatl_polygon


suffix = ['.tif', '.tiff']


class Management:
    @staticmethod
    def select_files_by_location(src_dir, location_path):
        file_paths = fileman.get_all_files(src_dir, suffix)
        location_ds = gpd.read_file(location_path)
        location_crs = location_ds.crs
        polygons = []
        for polygon in location_ds.geometry:
            polygons.append(polygon)
        location_multipolygon = shapely_geom.MultiPolygon(polygons)
        selected_files = []
        for file_path in file_paths['file']:
            with rasterio.open(file_path['path']) as src_ds:
                src_bounds = src_ds.bounds
                src_crs = src_ds.crs
                polygon = gatl_polygon.creat_from_bounds(src_bounds)
                df = pd.DataFrame({'name': [file_path['mname']],
                                   'bounds': [polygon]})
                dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='bounds')
                dst_gdf = dst_gdf.to_crs(location_crs)
                polygon = dst_gdf['bounds'][0]
                if location_multipolygon.intersects(polygon):
                    selected_files.append(file_path)
        return selected_files


class Extraction:
    @staticmethod
    def export_bounds(src_path, dst_dir):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            with rasterio.open(file_path['path']) as src_ds:
                src_bounds = src_ds.bounds
                src_crs = src_ds.crs
                polygon = gatl_polygon.creat_from_bounds(src_bounds)
                df = pd.DataFrame({'name': [file_path['mname']],
                                   'bounds': [polygon]})
                dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='bounds')
                dst_path = os.path.join(dst_dir, file_path['mname'] + '.shp')
                dst_gdf.to_file(dst_path)


if __name__ == '__main__':
    # Extraction.export_bounds(r'G:\RockGlacier\India\Himachal\GaoFen-1',
    #                          r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent')
    print(Management.select_files_by_location(r'G:\RockGlacier\India\Himachal\GaoFen-1',
                                              r'G:\RockGlacier\India\Himachal\Boundary\region.shp'))
    exit(0)
