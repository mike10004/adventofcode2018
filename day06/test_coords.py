#!/usr/bin/env python3

import sys
import math
import unittest
import io
from coords import Point, Edge, Grid

class PointTest(unittest.TestCase):

    def test_distance_instancemethod(self):
        d = Point(1, 1).distance(Point(2, 2))
        self.assertAlmostEquals(1.4142135623730951, d)
    
    def test_distance_classmethod(self):
        a = Point(1, 1)
        b = Point(2, 2)
        d = Point.distance(a, b)
        self.assertAlmostEquals(1.4142135623730951, d)
    
    def test_wrap(self):
        self.assertTrue(isinstance(Point.wrap((0, 0)), Point))
        p = Point(3, 4)
        self.assertTrue(p is Point.wrap(p))
        self.assertTrue(isinstance(Point.wrap([0, 0]), Point))

class EdgeTest(unittest.TestCase):

    def test_angle(self):
        u = Point(0, 0)
        v = Point(1, 1)
        w = Point(1, 0)
        p = Edge(u, v)
        q = Edge(u, w)
        a = p.angle(q)
        self.assertAlmostEqual(45.0, math.degrees(a))


def sample_grid():
        lines = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split("\n")
        points = [line.split(", ") for line in lines]
        points = [(int(x), int(y)) for (x, y) in points]
        points = [Point(*pair) for pair in points]
        grid = Grid.containing(points, (0, 0), (9, 9))
        return grid


class GridTest(unittest.TestCase):

    def test_find_owner(self):
        test_cases = [
            (Grid.containing([(0, 0)]), (0, 0), (0, 0)),
            (Grid.containing([(0, 0), (0, 1)]), (0, 0), (0, 0)),
            (Grid.containing([(0, 0), (0, 1)]), (0, 1), (0, 1)),
            (Grid.containing([(0, 0), (1, 1)]), (0, 0), (0, 0)),
            (Grid.containing([(0, 0), (1, 1)]), (1, 1), (1, 1)),
            (Grid.containing([(0, 0), (1, 1)]), (0, 1), None),
            (Grid.containing([(0, 0), (1, 1)]), (1, 0), None),
            (Grid.containing([(0, 0), (1, 0), (1, 3)]), (1, 0), (0, 0)),
            (Grid.containing([(0, 0), (1, 0), (1, 3)]), (1, 1), (1, 0)),
            (Grid.containing([(0, 0), (1, 0), (1, 3)]), (0, 3), (0, 0)),
        ]
        for grid, query, expected in test_cases:
            with self.subTest():
                actual = grid.find_owner(query)
                self.assertEqual(expected, actual, "in grid\n\n{}\n\nexpected {}, not {}, as owner of {} in {}".format(grid.rendering(), expected, actual, query, grid))


    def test_find_turf(self):
        g = sample_grid()
        for p in g.points:
            turf = g.find_turf(p)
            self.assertNotEqual(0, len(turf))
    
    def test_containing(self):
        g = Grid.containing([(1, 1)])
        self.assertEqual(1, g.size())
        self.assertEqual(1, len(g.points))
        self.assertIsInstance(g.points[0], Point)
        g = Grid.containing([(0, 0), (1, 1)])
        self.assertEqual(4, g.size())
        g = sample_grid()
    
    def test_render(self):
        g = sample_grid()
        ofile = io.StringIO()
        g.render(ofile)
        rendering = ofile.getvalue()
        print(rendering)
        expected = """aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
"""
        self.assertEqual(expected, rendering)

    def test_rendering(self):
        g = Grid.containing([(0, 0), (1, 0), (1, 4)])
        self.assertEqual(2, g.width, "width")
        self.assertEqual(5, g.height, "height")
        expected = """AB
ab
a.
cc
cC
"""
        self.assertEqual(expected, g.rendering())

    def test_rendering2(self):
        g = Grid.containing([(1, 1), (3, 4)], (0, 0), (4, 4))
        self.assertEqual(5, g.width, "width")
        self.assertEqual(5, g.height, "height")
        expected = """aaaaa
aAaaa
aaadd
aaddd
dddDd
"""
        self.assertEqual(expected, g.rendering(labels="AD"))
    
    def test_rendering3(self):
        g = Grid.containing([(1, 1), (3, 4), (1, 6)], (0, 0), (4, 6))
        self.assertEqual(5, g.width, "width")
        self.assertEqual(7, g.height, "height")
        expected = """aaaaa
aAaaa
aaadd
aaddd
..dDd
bb.dd
bBb..
"""
        self.assertEqual(expected, g.rendering(labels="ADB"))
    
    def test_rendering4(self):
        g = Grid.containing([(1, 1), (1, 6),(8, 3), (3, 4),  ], (0, 0), (9, 6))
        self.assertEqual(10, g.width, "width")
        self.assertEqual(7, g.height, "height")
        expected = """
aaaaaacccc
aAaaaacccc
aaadd.cccc
aaddd.ccCc
..dDdd.ccc
bb.ddd.ccc
bBb....ccc
"""
        actual = g.rendering()
        print()
        print()
        print(expected)
        print()
        print(actual)

        self.assertEqual(expected.strip(), actual.strip())
    
    def test_find_turf_trivial(self):
        cases = [
            ([(0, 0)], (0, 0), [(0, 0)]),
            ([(0, 0), (1, 1)], (0, 0), [(0, 0)]),
            ([(0, 0), (1, 1)], (1, 1), [(1, 1)]),
            ([(0, 0), (1, 1)], (1, 1), [(1, 1)]),
        ]
        for points, query, expected in cases:
            with self.subTest():
                g = Grid.containing(points)
                turf = g.find_turf(query)
                self.assertEqual(expected, list(turf))