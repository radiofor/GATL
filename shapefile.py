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
    def merge(src_dir, dst_path):
        file_paths = fileman.get_all_files(src_dir, suffix)
        dst_crs = gpd.read_file(file_paths['file'][0]['path']).crs
        dst_gdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(x['path']) for x in file_paths['file']], ignore_index=True),
                                   crs=dst_crs)
        dst_gdf.to_file(dst_path)


class Geoprocessing:
    @staticmethod
    def disolve(src_path, dst_dir, fields, continent, aggfunc):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            src_gdf = gpd.read_file(file_path['path'])
            fields.append('geometry')
            src_gdf = src_gdf[fields]
            if continent is None:
                src_gdf['disolve'] = [1] * src_gdf.count()[0]
                continent = 'disolve'
            src_gdf = src_gdf.dissolve(by=continent, aggfunc=aggfunc)
            src_gdf = src_gdf[fields]

            dst_dic = {}
            keys = [x for x in src_gdf.keys()]
            for key in keys:
                dst_dic[key] = []
            keys.remove('geometry')
            for iloc in src_gdf.iloc:
                geoms = list(iloc['geometry'])
                count = len(geoms)
                dst_dic['geometry'] += geoms
                for key in keys:
                    dst_dic[key] += [iloc[key]] * count

            dst_df = pd.DataFrame(dst_dic)
            dst_gdf = gpd.GeoDataFrame(dst_df, crs=src_gdf.crs, geometry='geometry')
            dst_path = os.path.join(dst_dir, file_path['fname'])
            dst_gdf.to_file(dst_path)


if __name__ == '__main__':
    # Management.merge(r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent',
    #                  r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent\tiles.shp')
    Geoprocessing.disolve(r'G:\ResearchArea\Nepal\VOC_L\segm_val\segm_val.shp', r'G:\ResearchArea\Nepal\VOC_L', ['FID'], None, 'first')
    exit(0)
