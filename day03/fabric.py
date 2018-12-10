#!/usr/bin/env python3

import sys
import re
import logging
from collections import defaultdict

_log = logging.getLogger(__name__)



class Square(tuple):

    col = None
    row = None

    def __new__(cls, col, row):
        thing = super(Square, cls).__new__(cls, tuple([col, row]))
        thing.__setattr__('col', col)
        thing.__setattr__('row', row)
        return thing


class Claim(tuple):

    claim_id = None
    corner = None
    width = None
    height = None

    def __new__(cls, claim_id, corner, width, height):
        claim = super(Claim, cls).__new__(cls, tuple([corner, width, height, claim_id]))
        claim.__setattr__('claim_id', claim_id)
        claim.__setattr__('corner', corner)
        claim.__setattr__('width', width)
        claim.__setattr__('height', height)
        return claim
    
    def squares(self):
        squares = []
        for col in range(self.corner.col, self.corner.col + self.width):
            for row in range(self.corner.row, self.corner.row + self.height):
                squares.append(Square(col, row))
        return tuple(squares)
    
    def intersection(self, other, overlap_id=0):
        mine = set(self.squares())
        theirs = set(other.squares())
        common = mine & theirs
        min_col, min_row = min([sq.col for sq in common]), min([sq.row for sq in common])
        max_col, max_row = max([sq.col for sq in common]), max([sq.row for sq in common])
        width, height = max_row - min_row + 1, max_col - min_col + 1
        return Claim(overlap_id, Square(min_col, min_row), width, height)
        

    @classmethod
    def parse(cls, token):
        """Parses a claim from a string like 
        
            #1 @ 1,3: 4x4

        """
        m = re.fullmatch(r'\s*#(?P<claim_id>\d+)\s+@\s+(?P<col>\d+),(?P<row>\d+):\s*(?P<width>\d+)x(?P<height>\d+)\s*', token)
        if m is None:
            return None
        claim_id = int(m.group('claim_id'))
        corner = Square(int(m.group('col')), int(m.group('row')))
        width, height = int(m.group('width')), int(m.group('height'))
        return Claim(claim_id, corner, width, height)


def main():
    logging.basicConfig(level=logging.DEBUG)
    _log.debug("reading from standard input")
    claims = [Claim.parse(line) for line in sys.stdin]
    counts = defaultdict(int)
    for claim in claims:
        squares = claim.squares()
        for sq in squares:
            counts[sq] += 1
    num_multiclaimed_squares = 0
    for sq, count in counts.items():
        if count > 1:
            num_multiclaimed_squares += 1
    print("{} of {} squares are contained in multiple claims".format(num_multiclaimed_squares, len(counts)))
    return 0

if __name__ == '__main__':
    exit(main())