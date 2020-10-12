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
    def extent_polygon(ncol, nrow, geotrsfrm):
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
            src_ds = gdal.Open(file_path['path'])
            if src_ds is None:
                continue
            ncol = src_ds.RasterXSize
            nrow = src_ds.RasterYSize
            geotrsfrm = src_ds.GetGeoTransform()
            srs = osr.SpatialReference(wkt=src_ds.GetProjection())

            dst_name = file_path['name'] + '.shp'
            driver = ogr.GetDriverByName("ESRI Shapefile")
            dst_ds = driver.CreateDataSource(os.path.join(dst_path, dst_name))
            dst_layer = dst_ds.CreateLayer('extent', srs=srs)
            dst_feat = ogr.Feature(dst_layer.GetLayerDefn())

            polygon = Extraction.extent_polygon(ncol, nrow, geotrsfrm)
            dst_feat.SetGeometry(polygon)
            dst_layer.CreateFeature(dst_feat)


if __name__ == '__main__':
    Extraction.export_extent(r'J:\QZGY2m-1', r'J:\Extent')
