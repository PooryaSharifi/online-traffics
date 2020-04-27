from random import random
import numpy as np


def inside(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def rectangle(points):
    X = [p[0] for p in points]
    Y = [p[1] for p in points]
    min_x = min(X)
    max_x = max(X)
    min_y = min(Y)
    max_y = max(Y)
    return [min_x, min_y], [max_x, max_y]


def rnd(points):
    _min, _max = rectangle(points)
    while True:
        x = (_max[0] - _min[0]) * random() + _min[0]
        y = (_max[1] - _min[1]) * random() + _min[1]
        if inside(x, y, points):
            return [x, y]


def grid_points(rec, resolution):
    min_x = rec[0][0]
    min_y = rec[0][1]
    max_x = rec[1][0]
    max_y = rec[1][1]
    resolution_x = resolution
    resolution_y = resolution
    X = np.arange(min_x + resolution_x / 2, max_x - resolution_x / 2, resolution_x)
    Y = np.arange(min_y + resolution_y / 2, max_y - resolution_y / 2, resolution_y)
    return [[[x, y, -1] for y in Y] for x in X]
