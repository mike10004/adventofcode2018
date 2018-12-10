#!/usr/bin/env python3

import sys
import re
import logging
from collections import defaultdict
import argparse


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
        if not common:
            return None
        min_col, min_row = min([sq.col for sq in common]), min([sq.row for sq in common])
        max_col, max_row = max([sq.col for sq in common]), max([sq.row for sq in common])
        width, height = max_row - min_row + 1, max_col - min_col + 1
        assert width > 0 and height > 0
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
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=('1', '2'), help="part ('1' or '2')")
    parser.add_argument("--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO')
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    _log.debug("reading from standard input")
    claims = [Claim.parse(line) for line in sys.stdin]
    if args.part == '1':
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
    elif args.part == '2':
        for i in range(len(claims)):
            a = claims[i]
            has_conflict = False
            for j in range(len(claims)):
                if i == j:
                    continue
                b = claims[j]
                if a.intersection(b) is not None:
                    _log.debug("{} of {}: {} intersects {}".format(i, len(claims), a, b))
                    has_conflict = True
                    break
            if not has_conflict:
                print("claim with no conflicts: {}".format(a))
                break
    else:
        raise ValueError("invalid part")
    return 0

if __name__ == '__main__':
    exit(main())