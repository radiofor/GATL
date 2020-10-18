# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
import time
import numpy as np
from skimage import io
import rasterio
from rasterio import features as rasterio_feat
import pandas as pd
import geopandas as gpd
from shapely import geometry as shapely_geom
import fileman
from georeferencing import Transform as gatl_transform
from geometry import Polygon as gatl_polygon


suffix = ['.tif', '.tiff']


class Management:
    @staticmethod
    def select_files_by_location(src_dir, location_path):
        location_ds = gpd.read_file(location_path)
        location_crs = location_ds.crs
        polygons = []
        for polygon in location_ds.geometry:
            polygons.append(polygon)
        location_multipolygon = shapely_geom.MultiPolygon(polygons)

        selected_files = []
        file_paths = fileman.get_all_files(src_dir, suffix)
        for file_path in file_paths['file']:
            src_ds = rasterio.open(file_path['path'])
            src_bounds = src_ds.bounds
            src_crs = src_ds.crs
            polygon = gatl_polygon.creat_from_bounds(src_bounds)
            df = pd.DataFrame({'name': [file_path['mname']], 'geometry': [polygon]})
            dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='geometry')
            dst_gdf = dst_gdf.to_crs(location_crs)
            polygon = dst_gdf['geometry'][0]
            if location_multipolygon.intersects(polygon):
                selected_files.append(file_path)
        return selected_files

    @staticmethod
    def create_by_image_and_worldfile(img_dir, wf_dir, img_suffix, wf_suffix, crs, dst_dir):
        src_paths = [img_dir, wf_dir]
        src_suffixs = [img_suffix, wf_suffix]
        file_paths = fileman.get_ruled_files(src_paths, src_suffixs, 'intersection')
        for mname in file_paths['mname']:
            img_path = os.path.join(img_dir, mname + img_suffix)
            img_ds = io.imread(img_path)
            img_height, img_width = img_ds.shape[:2]
            if len(img_ds.shape) == 2:
                img_ds.resize(img_height, img_width, 1)
            img_count = img_ds.shape[2]

            wf_path = os.path.join(wf_dir, mname + wf_suffix)
            transform = gatl_transform.from_worldfile(wf_path)

            dst_path = os.path.join(dst_dir, mname + suffix[0])
            dst_ds = rasterio.open(dst_path, 'w', driver='GTiff', height=img_height, width=img_width, count=img_count,
                                   dtype=img_ds.dtype, crs=crs, transform=transform)
            for i in range(img_count):
                dst_ds.write(img_ds[:, :, i], i + 1)

    @staticmethod
    def create_by_image_and_geodata(img_dir, gdt_dir, img_suffix, gdt_suffix, dst_dir):
        src_paths = [img_dir, gdt_dir]
        src_suffixs = [img_suffix, gdt_suffix]
        file_paths = fileman.get_ruled_files(src_paths, src_suffixs, 'intersection')
        for mname in file_paths['mname']:
            img_path = os.path.join(img_dir, mname + img_suffix)
            img_ds = io.imread(img_path)
            img_height, img_width = img_ds.shape[:2]
            if len(img_ds.shape) == 2:
                img_ds.resize(img_height, img_width, 1)
            img_count = img_ds.shape[2]

            gdt_path = os.path.join(gdt_dir, mname + gdt_suffix)
            gdt_ds = rasterio.open(gdt_path)
            crs = gdt_ds.crs
            transform = gdt_ds.transform

            dst_path = os.path.join(dst_dir, mname + suffix[0])
            dst_ds = rasterio.open(dst_path, 'w', driver='GTiff', height=img_height, width=img_width, count=img_count,
                                   dtype=img_ds.dtype, crs=crs, transform=transform)
            for i in range(img_count):
                dst_ds.write(img_ds[:, :, i], i + 1)

    @staticmethod
    def set_nodata_value(src_path, ndv):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            src_ds = rasterio.open(file_path['path'], 'r+')
            src_ds.nodata = ndv

    @staticmethod
    def convert_to_shapefile(src_path, bands, dst_dir):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            src_ds = rasterio.open(file_path['path'])
            src_ndv = src_ds.nodata
            src_crs = src_ds.crs
            src_transform = src_ds.transform
            for i in bands:
                src_band = src_ds.read(i)
                mask = src_band != src_ndv
                src_shapes = list(rasterio_feat.shapes(src_band, mask=mask, transform=src_transform))
                src_shapes = [x[0] for x in src_shapes]
                src_polygons = [shapely_geom.shape(x) for x in src_shapes]
                df = pd.DataFrame({'geometry': src_polygons})
                dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='geometry')
                if len(bands) == 1:
                    dst_name = file_path['mname'] + '.shp'
                else:
                    dst_name = '{0}_{1}.shp'.format(file_path['mname'], str(i))
                dst_path = os.path.join(dst_dir, dst_name)
                dst_gdf.to_file(dst_path)


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
                                   'geometry': [polygon]})
                dst_gdf = gpd.GeoDataFrame(df, crs=src_crs, geometry='geometry')
                dst_path = os.path.join(dst_dir, file_path['mname'] + '.shp')
                dst_gdf.to_file(dst_path)


if __name__ == '__main__':
    # Extraction.export_bounds(r'G:\RockGlacier\India\Himachal\GaoFen-1',
    #                          r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent')
    # print(Management.select_files_by_location(r'G:\RockGlacier\India\Himachal\GaoFen-1',
    #                                           r'G:\RockGlacier\India\Himachal\Boundary\region.shp'))
    # Management.create_by_image_and_worldfile(r'G:\Test', r'G:\Test', '.jpg', '.jgw', 'epsg:3857', r'G:\Test')
    # Management.set_nodata_value(r'G:\Test\binary.tif', 0)
    Management.convert_to_shapefile(r'G:\Test\binary.tif', [1], r'G:\Test')
    exit(0)
