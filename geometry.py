# -*- coding: utf-8 -*-
import os
import fileman
from shapely import geometry as shapely_geom


class Polygon:
    @staticmethod
    def creat_from_bounds(bounds):
        polygon = shapely_geom.Polygon([(bounds[0], bounds[1]),
                                        (bounds[2], bounds[1]),
                                        (bounds[2], bounds[3]),
                                        (bounds[0], bounds[3])])
        return polygon

    @staticmethod
    def polygons_to_multipolygon(polygons):
        polygons



if __name__ == '__main__':
    Polygon.creat_from_bounds((-2702192.0, 3819192.0, -2622192.0, 3899192.0))
    exit(0)
