# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
import time
import fileman
import pandas as pd
import geopandas as gpd

suffix = ['.shp']


class Management:
    @staticmethod
    def merge(src_path, dst_path):
        file_paths = fileman.get_all_files(src_path, suffix)
        dst_gdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(x['path']) for x in file_paths['file']], ignore_index=True),
                                   crs=gpd.read_file(file_paths['file'][0]['path']).crs)
        dst_gdf.to_file(dst_path)


class Geoprocessing:
    @staticmethod
    def disolve(src_path):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            continue


if __name__ == '__main__':
    Management.merge(r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent',
                     r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent\tiles.shp')
    exit(0)
