# -*- coding: utf-8 -*-
import fileman
import geotiff


selected_file = geotiff.Management.select_files_by_location(r'I:\QZGY2m-2', r'')
fileman.copy_files(selected_file, r'G:\RockGlacier\Nyenchenthanglha\GaoFen-1')
