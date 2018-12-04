#!/usr/bin/env python3

import unittest
import io
import rudisum
import argparse
from rudisum import RepeatCharPredicate

class TestRepeatCharPredicate(unittest.TestCase):

    def test_something(self):
        p = RepeatCharPredicate()
        self.assertEqual('', p.evaluate('abcdef', 2))
        self.assertEqual('', p.evaluate('abcdef', 3))
        self.assertEqual('a', p.evaluate('bababc', 2))
        self.assertEqual('b', p.evaluate('bababc', 3))
        self.assertEqual('b', p.evaluate('abbcde', 2))
        self.assertEqual('', p.evaluate('abbcde', 3))
        self.assertEqual('c', p.evaluate('abcccd', 3))
        self.assertEqual('', p.evaluate('abcccd', 2))
        self.assertEqual('e', p.evaluate('abcdee', 2))
        self.assertEqual('ab', p.evaluate('ababab', 3))
        self.assertEqual('', p.evaluate('ababab', 2))


class TestComputeChecksum(unittest.TestCase):
    
    def test_something(self):
        sequences = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
""".split()
        sequences = [s.strip() for s in sequences]
        checksum = rudisum.compute_checksum(sequences, (2, 3,))
        self.assertEqual(12, checksum)