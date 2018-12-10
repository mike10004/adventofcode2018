#!/usr/bin/env python3

import unittest
from fabric import Claim, Square

class TestSquare(unittest.TestCase):

    def test_create(self):
        u = Square(2, 3)
        v = Square(5, 6)
        w = Square(2, 3)
        self.assertEqual(u, w)
        self.assertNotEqual(u, v) 
        self.assertNotEqual(v, w) 

class TestClaim(unittest.TestCase):

    def test_parse(self):
        claim = Claim.parse('#1 @ 1,3: 4x4')
        self.assertEqual(Claim(1, Square(1, 3), 4, 4), claim)

    def test_squares(self):
        c = Claim(1, Square(1, 3), 2, 2)
        expected = set([Square(1, 3), Square(2, 3), Square(1, 4), Square(2, 4)])
        actual = set(c.squares())
        self.assertEqual(expected, actual, "{} != {}".format(expected, actual))
    
    def test_intersection(self):
        claim1 = Claim(1, Square(1, 3), 4, 4)
        claim2 = Claim(2, Square(3, 1), 4, 4)
        expected = Claim(-1, Square(3, 3), 2, 2)
        actual = claim1.intersection(claim2, -1)
        self.assertEqual(expected, actual)

