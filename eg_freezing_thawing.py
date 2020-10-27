# -*- coding: utf-8 -*-
import os
import rasterio
import numpy as np


src_dir = r'G:\GeoBaseData\中国冻融地表数据集\TIF'
src_fnames = os.listdir(src_dir)
src_fnames.sort(key=lambda x: int(x.rsplit('.')[0]))
src_paths = [os.path.join(src_dir, x) for x in src_fnames if x.rsplit('.', 1)[1] == 'tif']
print(src_paths)
src_ds = rasterio.open(src_paths[0])
src_band = src_ds.read(1)
height = src_ds.height
width = src_ds.width
dst_path = r'G:\GeoBaseData\中国冻融地表数据集\whole.tif'
if os.path.exists(dst_path):
    os.remove(dst_path)
dst_ds = rasterio.open(dst_path, 'w', driver='GTiff', height=height, width=width,
                       count=src_ds.count, dtype=src_band.dtype, crs=src_ds.crs,
                       transform=src_ds.transform)
dst_band = np.zeros([height, width], np.int32)
src_ds = None
k = 0
band = np.zeros([height, width], np.int32)
for src_path in src_paths:
    if k == 7:
        k = 0
        dst_band += band
        band = np.zeros([height, width], np.int32)
    src_ds = rasterio.open(src_path)
    src_band = src_ds.read(1)
    band[src_band == 1] = 7
    k += 1
dst_ds.write(dst_band, 1)
dst_ds.nodata = 0
