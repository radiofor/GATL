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

    @staticmethod
    def clip_by_polygon(src_path, loc_path, dst_dir, data_name, band_codes, clip_size, overlay_size):
        src_ds = rasterio.open(src_path)
        transform = src_ds.transform
        # max_y, min_x
        src_leftup = [transform[5], transform[2]]
        px_geosize = [-transform[4], transform[0]]
        clip_geosize = [a * b for a, b in zip(clip_size, px_geosize)]
        overlay_geosize = [a * b for a, b in zip(overlay_size, px_geosize)]
        offset_geosize = [a - b for a, b in zip(clip_geosize, overlay_geosize)]

        src_bands = []
        count = len(band_codes)
        for i in range(count):
            src_bands.append(src_ds.read(band_codes[i]))
        src_dtype = src_bands[0].dtype

        loc_ds = gpd.read_file(loc_path)
        geoms = [x for x in loc_ds.geometry]
        loc_polygon = shapely_geom.MultiPolygon(geoms)
        loc_bounds = loc_ds.bounds
        bounds = [loc_bounds['minx'][0], loc_bounds['miny'][0],
                  loc_bounds['maxx'][0], loc_bounds['maxy'][0]]
        clip_count = [int((bounds[3] - bounds[1]) / offset_geosize[0]) + 1,
                      int((bounds[2] - bounds[0]) / offset_geosize[1]) + 1]

        for i in range(clip_count[0]):
            for j in range(clip_count[1]):
                # 待裁剪影像的坐标范围[min_x, min_y, max_x, max_y]
                clip_bounds = (bounds[0] + offset_geosize[0] * j,
                               bounds[3] - offset_geosize[0] * i - clip_geosize[0],
                               bounds[0] + offset_geosize[0] * j + clip_geosize[1],
                               bounds[3] - offset_geosize[0] * i)
                clip_polygon = gatl_polygon.creat_from_bounds(clip_bounds)

                # 若该幅影像坐标范围不与任何Polygon相交，则跳过裁剪
                if not loc_polygon.intersects(clip_polygon):
                    continue

                # 设置名称
                clip_name = data_name + '_{0}_{1}'.format(str(i).zfill(3), str(j).zfill(3))

                # 创建World File
                with open(os.path.join(dst_dir, clip_name + '.jgw'), 'w') as f:
                    f.writelines([str(px_geosize[0]) + '\n', str(0) + '\n', str(0) + '\n',
                                  str(-px_geosize[1]) + '\n', str(clip_bounds[0]) + '\n', str(clip_bounds[3]) + '\n'])

                # max_y, min_x
                clip_pxleftup = [round((src_leftup[0] - clip_bounds[3]) / px_geosize[0]),
                                 round((clip_bounds[0] - src_leftup[1]) / px_geosize[1])]

                clip_data = np.zeros(clip_size + [count], src_dtype)
                for k in range(count):
                    clip_data[:, :, k] = src_bands[k][clip_pxleftup[0]: clip_pxleftup[0] + clip_size[0],
                                         clip_pxleftup[1]: clip_pxleftup[1] + clip_size[1]]
                clip_path = os.path.join(dst_dir, clip_name + '.jpg')
                io.imsave(clip_path, clip_data)


if __name__ == '__main__':
    # Extraction.export_bounds(r'G:\RockGlacier\India\Himachal\GaoFen-1',
    #                          r'G:\RockGlacier\India\Himachal\GaoFen-1\Extent')
    # print(Management.select_files_by_location(r'G:\RockGlacier\India\Himachal\GaoFen-1',
    #                                           r'G:\RockGlacier\India\Himachal\Boundary\region.shp'))
    # Management.create_by_image_and_worldfile(r'G:\Test', r'G:\Test', '.jpg', '.jgw', 'epsg:3857', r'G:\Test')
    # Management.set_nodata_value(r'G:\RockGlacier\Nyenchenthanglha\GaoFen-1\Nyenchenthanglha.tif', 0)
    # Management.convert_to_shapefile(r'G:\Test\binary.tif', [1], r'G:\Test')
    Extraction.clip_by_polygon(r'G:\RockGlacier\Nyenchenthanglha\GaoFen-1\Nyenchenthanglha_3857.tif',
                               r'G:\RockGlacier\Nyenchenthanglha\Boundary\bounds_3857.shp',
                               r'G:\RockGlacier\Nyenchenthanglha\GaoFen-1\JPG',
                               'Nyenchenthanglha', [1], [1000, 1000], [200, 200])
    exit(0)
