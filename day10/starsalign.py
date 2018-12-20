#!/usr/bin/env python3

import os
import io
import re
import sys
import math
import logging
import logging
import argparse


_log = logging.getLogger(__name__)


class Star(tuple):

    position, velocity = [], tuple()

    def __new__(cls, position, velocity):
        me = super(Star, cls).__new__(cls, [position, velocity])
        me.position = list(position)
        me.velocity = velocity
        return me
    
    @classmethod
    def parse(cls, text):
        m = re.fullmatch(r'\s*position=<\s*(-?\d+)\s*,\s*(-?\d+)\s*>\s+velocity=<\s*(-?\d+)\s*,\s*(-?\d+)\s*>\s*', text.strip())
        assert m is not None, "text does not match expected pattern: {}".format(repr(text))
        px, py = int(m.group(1)), int(m.group(2))
        vx, vy = int(m.group(3)), int(m.group(4))
        return Star((px, py), (vx, vy))
    
    @classmethod
    def parse_many(cls, ifile):
        return [Star.parse(line) for line in ifile if line.strip()]
    
    def tick(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        return self


class Processor(object):

    def __init__(self):
        pass
    
    def tick(self, stars):
        for star in stars:
            star.tick()
    
    def render(self, stars, ofile=sys.stdout, width=80, height=None, shades=('.', '#')):
        if height is None:
            height = max([star.position.y for star in stars])
        dark, light = shades[0], shades[-1]
        stars_by_position = {}
        for star in stars:
            stars_by_position[tuple(star.position)] = star
        for y in range(height):
            for x in range(width):
                star = stars_by_position.get((x, y))
                mark = light if star else dark
                print(mark, end="", file=ofile)
            print(file=ofile)    
        
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    parser.add_argument("-t", "--truncate", type=int, help="truncate at column N", metavar='N', default=79)
    parser.add_argument("--rows", type=int, help="set fixed number of rows", default=None)
    parser.add_argument("input_file", help="input text file pathname", metavar='FILE')
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    with open(args.input_file, 'r') as ifile:
        stars = Star.parse_many(ifile)
    intext = ''
    processor = Processor()
    ofile = sys.stdout
    while not intext.strip():
        processor.render(stars, ofile, width=args.truncate, height=args.rows)
        print(file=ofile)
        intext = input("Press enter to proceed ")
        print(file=ofile)
        _log.debug("input: %r", intext)
        processor.tick(stars)
    print("done")
    return 0


if __name__ == '__main__':
    exit(main())
