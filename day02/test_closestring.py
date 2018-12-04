#!/usr/bin/env python3

import unittest
import closestring

class TestFindDistances(unittest.TestCase):

    def test_something(self):
        sequences = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".split()
        distances = closestring.find_distances(sequences)
        # expected = {

        # }
        # self.assertDictEqual(expected, distances)
        for k, ds in distances.items():
            print(k, ds)
