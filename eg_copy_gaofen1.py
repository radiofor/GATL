# -*- coding: utf-8 -*-
import geotiff
import fileman


selected_files = geotiff.Management.select_files_by_location(r'I:\QZGY2m-2', r'G:\RockGlacier\Nyenchenthanglha\Boundary\bounds.shp')
fileman.copy_files(selected_files, r'G:\RockGlacier\Nyenchenthanglha\GaoFen-1')