#!/usr/bin/env python3

import os
import io
import re
import sys
import math
import logging
import logging
import argparse
from PIL import Image
from collections import defaultdict


_log = logging.getLogger(__name__)


class Star(object):

    def __init__(self, position, velocity):
        self.position = list(position)
        self.velocity = tuple(velocity)
    
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
    
    @classmethod
    def tick_all(cls, stars):
        for star in stars:
            star.tick()


class Renderer(object):

    def __init__(self):
        pass
    
    def print(self, stars, ofile=sys.stdout, width=80, height=40, shades=('.', '#')):
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
    
    def draw(self, stars, output_pathname, predicate, simulate=False):
        min_x = min([star.position[0] for star in stars])
        max_x = max([star.position[0] for star in stars])
        min_y = min([star.position[1] for star in stars])
        max_y = max([star.position[1] for star in stars])
        width, height = max_x - min_x, max_y - min_y
        if not predicate(stars, width, height):
            _log.debug("skipping image too large: {}x{}".format(width, height))
            return
        empty, nonempty = 1, 0
        if simulate:
            _log.debug("would have written %sx%s image of %s stars", width, height, len(stars))
            return 1
        image = Image.new('1', (width + 1, height + 1), empty)
        for star in stars:
            x, y = star.position[0] - min_x, star.position[1] - min_y
            image.putpixel((x, y), nonempty)
        output_dir = os.path.dirname(output_pathname)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        image.save(output_pathname)        
        return image


class DrawPredicate(object):

    def __init__(self, args):
        self.args = args

    def _contains_line(self, stars, pos=0):
        assert self.args.min_line is not None
        by_coord = defaultdict(int)
        for star in stars:
            by_coord[star.position[pos]] += 1
        for length in by_coord.values():
            if length >= self.args.min_line:
                return True
        return False
    
    def __call__(self, *params):
        stars, width, height = params
        if self.args.max_dim > 0:
            if width > self.args.max_dim or height > self.args.max_dim:
                return False
        if self.args.min_line is not None:
            return self._contains_line(stars, 0) or self._contains_line(stars, 1)
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    parser.add_argument("--cols", "--columns", type=int, dest="columns", help="set fixed number of columns", metavar='N', default=79)
    parser.add_argument("--image", dest='mode', action='store_const', const='image')
    parser.add_argument("--image-prefix", default="/tmp/starsalign/image-")
    parser.add_argument("--image-suffix", default=".png")
    parser.add_argument("--simulate", action='store_true', help="in 'image' mode, do not write images, but describe them")
    parser.add_argument("--max-dim", type=int, default=50000, help="max pixels in either image dimension (otherwise skip)")
    parser.add_argument("--iterations", type=int, default=100, help="number of iterations in image mode")
    parser.add_argument("--rows", type=int, help="set fixed number of rows", default=40)
    parser.add_argument("--min-line", type=int, help="set minimum line length predicate", default=None)
    parser.add_argument("input_file", help="input text file pathname", metavar='FILE')
    parser.add_argument("mode", choices=('text', 'image'))
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    with open(args.input_file, 'r') as ifile:
        stars = Star.parse_many(ifile)
    intext = ''
    renderer = Renderer()
    if args.mode == 'text':
        ofile = sys.stdout
        while not intext.strip():
            renderer.print(stars, ofile, width=args.columns, height=args.rows)
            print(file=ofile)
            intext = input("Press enter to proceed ")
            print(file=ofile)
            _log.debug("input: %r", intext)
            Star.tick_all(stars)
        print("done")
    elif args.mode == 'image':
        ncreated = 0
        predicate = DrawPredicate(args)
        for i in range(args.iterations):
            pn = "{}{}{}".format(args.image_prefix, i, args.image_suffix)
            image = renderer.draw(stars, pn, predicate, args.simulate)
            ncreated += (1 if image else 0)
            Star.tick_all(stars)
        _log.debug("%s of %s images created", ncreated, args.iterations)
        if args.simulate:
            print("{} images created".format(ncreated))
        if ncreated == 0:
            _log.warn("zero images created")
            return 2
    else:
        raise NotImplementedError()
    return 0


if __name__ == '__main__':
    exit(main())
