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
    def disolve(src_path, dst_dir, fields, continent, aggfunc):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            src_gdf = gpd.read_file(file_path['path'])
            fields.append('geometry')
            src_gdf = src_gdf[fields]
            src_gdf = src_gdf.dissolve(by=continent, aggfunc=aggfunc)
            dst_path = os.path.join(dst_dir, file_path['fname'])
            src_gdf.to_file(dst_path)


if __name__ == '__main__':
    # Management.merge(r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent',
    #                  r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent\tiles.shp')
    Geoprocessing.disolve(r'G:\Test\gadm36_IND_2.shp', r'G:\Test\Dissolve', ['NAME_0', 'NAME_1', 'NAME_2'], 'NAME_1', 'sum')
    exit(0)
