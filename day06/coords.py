#!/usr/bin/env python3

import sys
import io
import math
import logging
from collections import defaultdict
from operator import itemgetter


_ctype = int  # type of a component of a coordinate pair
_log = logging.getLogger(__name__)


def sq(x):
    return x * x


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
    
    def border(self):
        min_x, min_y = self.corner
        max_x, max_y = min_x + self.width - 1, min_y + self.height - 1
        x_range = list(range(min_x, max_x + 1))
        y_range = list(range(min_y, max_y + 1))
        pts = (
            [(min_x, y) for y in y_range] +
            [(x, min_y) for x in x_range] +
            [(max_x, y) for y in y_range] + 
            [(x, max_y) for x in x_range]
        )
        return sorted(set(pts))
    
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

    def distance_sum(self, p, dist_fn=Point.manhattan):
        s = 0
        for q in self.points:
            s += dist_fn(q, p)
        return s
    
    def region_size(self, max_dist, dist_fn=Point.manhattan):
        region_size = 0
        for y in range(self.corner.y, self.corner.y + self.height):
            for x in range(self.corner.x, self.corner.x + self.width):
                not_in_region = False
                total_dist = self.distance_sum((x, y), dist_fn)
                if total_dist < max_dist:
                    region_size += 1
        return region_size

    

def parse_coords(ifile, ctype=_ctype):
    """Parses a list of coordinate pairs."""
    points = [tuple(map(ctype, pair.split(", "))) for pair in ifile if pair]
    points = [Point(*pair) for pair in points]
    return points


def find_max_finite_area(grid):
    max_area, max_owner = None, None
    border = grid.border()
    nignored = 0
    for p in grid.points:
        turf = grid.find_turf(p)
        turf_on_border = False
        for t in turf:
            if t in border:
                turf_on_border = True
                break
        if turf_on_border:
            nignored += 1
            continue
        area = len(turf)
        _log.debug("{} has turf with area {}".format(p, area))
        if max_area is None or area > max_area:
            max_area = area
            max_owner = p
    _log.debug("ignored %d points in search for max finite area", nignored)
    return max_owner, max_area


def part1(grid, args):
    max_owner, max_area = find_max_finite_area(grid)
    assert max_owner is not None, "no max owner found; no finite areas?"
    print("{} has turf with max area {}".format(max_owner, max_area))


def part2(grid, args):
    region_size = grid.region_size(args.max_dist)
    print("max region size with dist < {} is {}".format(args.max_dist, region_size))

        
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int, choices=(1, 2))
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("--max-dist", type=int, default=10000)
    args = parser.parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))
    coord_pairs = parse_coords(sys.stdin)
    _log.debug("%s points in input", len(coord_pairs))
    grid = Grid.containing(coord_pairs)
    part = {
        1: part1,
        2: part2,
    }[args.part]
    part(grid, args)
    return 0


if __name__ == '__main__':
    exit(main())
