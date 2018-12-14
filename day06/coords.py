#!/usr/bin/env python3

import sys
import io
import math
import pyhull
from collections import defaultdict
from operator import itemgetter


def sq(x):
    return x * x


def magnitude(p):
    """Calculates the magnitude of a vector p."""
    return math.sqrt(sq(p[0]) + sq(p[1]))


def dot_product(p, q):
    assert len(p) == len(q), "vectors are not congruent"
    s = 0
    for i in range(len(p)):
        s += (p[i] * q[i])
    return s


class Point(tuple):

    x, y = None, None

    def __new__(cls, x, y):
        me = super(Point, cls).__new__(cls, [x, y])
        me.x = x
        me.y = y
        return me
    
    @classmethod
    def manhattan(cls, p, q):
        return abs(p[0] - q[0]) + abs(p[1] - q[1])
    
    def distance(self, p, q=None):
        """Computes the distance between this point and another. Arguments can
        be tuples or Point instances. Returns a float.
        
        Can also be called as a class method, meaning Point(x1, y1).distance((x2, y2)) 
        is equivalent to Point.distance((x1, y1), (x2, y2)).
        """
        if type(self) == Point:
            q = p
            p = self
        p, q = Point.wrap(p), Point.wrap(q)
        return math.sqrt(sq(p.x - q.x) + sq(p.y - q.y))
    
    def scale(self, alpha):
        return Point(alpha * self.x, alpha * self.y)
    
    def translate(self, other):
        return Point(self.x + other[0], self.y + other[1])
    
    @classmethod
    def wrap(cls, point_or_tuple):
        if isinstance(point_or_tuple, Point):
            return point_or_tuple
        else:
            return Point(*point_or_tuple)
    

class Edge(tuple):

    u, v = None, None

    def __new__(cls, u, v):
        u = Point.wrap(u)
        v = Point.wrap(v)
        me = super(Edge, cls).__new__(cls, [u, v])
        me.u = u
        me.v = v
        return me
    
    def angle(self, adjacent):
        """Measures the angle between this edge and another that shares the same first endpoint."""
        assert self.u == adjacent.u, "argument edge's point u must equal this edge's point u "
        p = self.v.translate(self.u.scale(-1))
        q = adjacent.v.translate(self.u.scale(-1))
        cosa = dot_product(p, q) / (magnitude(p) * magnitude(q))
        return math.acos(cosa)


class Grid(object):

    def __init__(self, corner, width, height, points):
        self.corner = Point.wrap(corner)
        self.width = width
        self.height = height
        self.points = tuple([Point.wrap(p) for p in points])
        assert len(self.points) == len(set(self.points))
        self._cells = None
        self._cells_to_owners = None
        self.distance = Point.manhattan
    
    @classmethod
    def containing(cls, points, topleft=None, bottomright=None):
        if topleft is None:
            min_x, min_y = min([p[0] for p in points]), min([p[1] for p in points])
        else:
            min_x, min_y = topleft
        if bottomright is None:
            max_x, max_y = max([p[0] for p in points]), max([p[1] for p in points])
        else:
            max_x, max_y = bottomright
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        return Grid(Point(min_x, min_y), width, height, points)
    
    def size(self):
        return self.width * self.height
    
    def cells(self):
        if self._cells is None:
            cells = []
            for i in range(self.width):
                for j in range(self.height):
                    cells.append(self.corner.translate((i, j)))
            self._cells = tuple(cells)
        return self._cells
    
    def map_cells_to_owners(self):
        """Returns a dictionary mapping each cell to the point that is closest."""
        if self._cells_to_owners is None:
            owners = defaultdict(lambda: None)
            for cell in self.cells():
                owner = self.find_owner(cell)
                if owner is not None:
                    owners[cell] = owner
            self._cells_to_owners = owners
        return self._cells_to_owners    
    
    def find_owner(self, cell):
        cell = Point.wrap(cell)
        closest_p = None
        min_distance = None
        distance_counts = defaultdict(int)
        for p in self.points:
            distance = self.distance(cell, p)
            distance_counts[distance] += 1
            if min_distance is None or distance < min_distance:
                closest_p = p
                min_distance = distance
        if distance_counts[min_distance] > 1:
            return None
        return closest_p
        
    
    def find_turf(self, p):
        p = Point.wrap(p)
        cells_to_owners = self.map_cells_to_owners()
        turf = set()
        for cell in cells_to_owners:
            owner = cells_to_owners[cell]
            if p == owner:
                turf.add(cell)
        return turf
    
    def _create_label_map(self, labels=None):
        labels = labels or 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        label_map = {}
        n = 0
        for p in self.points:
            label_map[p] = labels[n]
            n += 1
        return label_map
    
    def render(self, ofile=sys.stdout, labels=None):
        label_map = self._create_label_map(labels)
        cells_to_owners = self.map_cells_to_owners()
        for j in range(self.height):
            for i in range(self.width):
                cell = self.corner.translate((i, j))
                owner = cells_to_owners[cell]
                label = label_map[owner] if owner is not None else '.'
                if cell != owner:
                    label = label.lower()
                print(label, end='', file=ofile)
            print(file=ofile)
    
    def rendering(self, labels=None):
        buffer = io.StringIO()
        self.render(buffer, labels)
        return buffer.getvalue()


        



    

