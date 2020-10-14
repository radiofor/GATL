# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
import time
import numpy as np
import imageio
import rasterio
import pandas as pd
import geopandas as gpd
import fileman
import geometry as gatl_geom


suffix = ['.tif', '.tiff']


class Extraction:
    @staticmethod
    def export_bounds(src_path, dst_dir):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            with rasterio.open(file_path['path']) as src_ds:
                if src_ds is None:
                    continue
                src_bounds = src_ds.bounds
                src_crs = src_ds.crs
                polygon = gatl_geom.bounds_polygon(src_bounds)
                df = pd.DataFrame({'name': [file_path['name']],
                                   'bounds': [polygon]})
                dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='bounds')
                dst_path = os.path.join(dst_dir, file_path['name'] + '.shp')
                dst_gdf.to_file(dst_path)


if __name__ == '__main__':
    Extraction.export_bounds(r'G:\RockGlacier\India\Himachal\GaoFen-1', r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent')
