# -*- coding: utf-8 -*-
import os
import fileman
import numpy as np
import imageio
from tqdm import tqdm
import time
from osgeo import gdal
from osgeo import osr
from osgeo import ogr


suffix = ['.tif', '.tiff']


class Extraction:
    @staticmethod
    def extent_polygon(src_path):
        with gdal.Open(src_path['path']) as src_ds:
            ncol = src_ds.RasterXSize
            nrow = src_ds.RasterYSize
            geotrsfrm = src_ds.GetGeoTransform()

            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(geotrsfrm[0], geotrsfrm[3])
            ring.AddPoint(geotrsfrm[0] + ncol * geotrsfrm[1], geotrsfrm[3])
            ring.AddPoint(geotrsfrm[0] + ncol * geotrsfrm[1], geotrsfrm[3] + nrow * geotrsfrm[5])
            ring.AddPoint(geotrsfrm[0], geotrsfrm[3] + nrow * geotrsfrm[5])
            ring.AddPoint(geotrsfrm[0], geotrsfrm[3])

            polygon = ogr.Geometry(ogr.wkbPolygon)
            polygon.AddGeometry(ring)

            return polygon


    @staticmethod
    def export_extent(src_path, dst_path):
        file_paths = fileman.get_all_files(src_path, suffix)
        for file_path in file_paths['file']:
            polygon =


if __name__ == '__main__':
    Extraction.layer_extent(r'I:\QZGY2m-1', r'I:')
