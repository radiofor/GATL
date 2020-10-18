# -*- coding: utf-8 -*-
import os
import rasterio


class Transform:
    @staticmethod
    def from_worldfile(wf_path):
        wf_paras = []
        with open(wf_path, 'r') as f:
            wf_para = f.readline()
            while wf_para:
                wf_paras.append(float(wf_para))
                wf_para = f.readline()
        transform = rasterio.Affine(wf_paras[0], wf_paras[1], wf_paras[4], wf_paras[2], wf_paras[3], wf_paras[5])
        return transform
