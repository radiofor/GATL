# -*- coding: utf-8 -*-
import os
import fileman
from tqdm import tqdm
import time
from osgeo import osr
from osgeo import ogr


suffix = ['.py']


class Geometry:
    @staticmethod
    def disolve(src_path):
        file_paths = fileman.get_all_files(r'F:\Projects\GATL', suffix)
        for file_path in file_paths['file']:
            driver = ogr.GetDriverByName("ESRI Shapefile")
            src_ds = driver.Open(src_path['path'], 0)

    @staticmethod
    def


if __name__ == '__main__':
    Geometry.disolve()
