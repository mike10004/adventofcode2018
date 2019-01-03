#!/usr/bin/env python3
#
# From redditor Shemetz on the solution megathread 
# https://www.reddit.com/r/adventofcode/comments/a5qd71/2018_day_13_solutions/
#

import sys
import os
import logging
import argparse
from typing import List, Tuple, Dict
from collections import defaultdict

_log = logging.getLogger(__name__)


class Cart:
    def __init__(self, pos: complex, di: complex):
        self.position = pos
        self.direction = di
        self.cross_mod = 0
        self.dead = False


def setup(input_file_lines: List[str]) -> Tuple[Dict[complex, str], List[Cart]]:
    tracks = defaultdict(lambda: "")  # only stores important tracks: \ / +
    carts = []
    for y, line in enumerate(input_file_lines):
        for x, char in enumerate(line):
            if char == "\n":
                continue
            if char in "<v>^":
                direction = {
                    "<": -1,
                    "v": +1j,
                    ">": +1,
                    "^": -1j,
                }[char]
                carts.append(Cart(x + y * 1j, direction))  # location, direction, crossings
                part = {
                    "<": "-",
                    "v": "|",
                    ">": "-",
                    "^": "|",
                }[char]
            else:
                part = char
            if part in "\\/+":
                tracks[(x + y * 1j)] = part
    return tracks, carts


def turn_cart(cart: Cart, part: str):
    """This space uses a downwards-facing Y axis, which means all calculations
    must flip their imaginary part. For example, rotation to the left
    (counterclockwise) would be multiplying by -1j instead of by +1j."""
    if not part:  # empty track is impossible, and | or - don't matter
        return
    if part == "\\":
        if cart.direction.real == 0:
            cart.direction *= -1j  # ⮡ ⮢
        else:
            cart.direction *= +1j  # ⮧ ⮤
    if part == "/":
        if cart.direction.real == 0:
            cart.direction *= +1j  # ⮣ ⮠
        else:
            cart.direction *= -1j  # ⮥ ⮦
    if part == "+":
        cart.direction *= -1j * 1j ** cart.cross_mod  # rotate left, forward, or right
        cart.cross_mod = (cart.cross_mod + 1) % 3


def solve_a(input_file_lines: List[str]) -> str:
    tracks, carts = setup(input_file_lines)
    while True:
        carts.sort(key=lambda c: (c.position.imag, c.position.real))
        for ci, cart in enumerate(carts):
            cart.position += cart.direction
            if any(c2.position == cart.position for c2i, c2 in enumerate(carts) if c2i != ci):
                return int(cart.position.real), int(cart.position.imag)
            part = tracks[cart.position]
            turn_cart(cart, part)


def solve_b(input_file_lines: List[str]) -> str:
    tracks, carts = setup(input_file_lines)
    while len(carts) > 1:
        carts.sort(key=lambda c: (c.position.imag, c.position.real))
        for ci, cart in enumerate(carts):
            if cart.dead:
                continue
            cart.position += cart.direction
            for ci2, cart2 in enumerate(carts):
                if ci != ci2 and cart.position == cart2.position and not cart2.dead:
                    cart.dead = True
                    cart2.dead = True
                    break
            if cart.dead:
                continue
            part = tracks[cart.position]
            turn_cart(cart, part)
        carts = [c for c in carts if not c.dead]
    if not carts:
        raise Exception("there's an even number of carts, there's isn't 1 cart left at the end!")
    cart = carts[0]
    return int(cart.position.real), int(cart.position.imag)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", metavar="FILE", default="/dev/stdin")
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    with open(args.input_file, 'r') as ifile:
        lines = [line for line in ifile]
    return 0

if __name__ == '__main__':
    exit(main())
