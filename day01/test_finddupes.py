#!/usr/bin/python3

import sys
import finddupes
import unittest

class TestFindDupes(unittest.TestCase):

    def test_examine3(self):
        dupe = finddupes.examine((-6, 3, 8, 5, -6))
        self.assertEqual(5, dupe)

    def test_examine4(self):
        dupe = finddupes.examine((7, 7, -2, -7, -4))
        self.assertEqual(14, dupe)
