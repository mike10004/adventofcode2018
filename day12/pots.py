#!/usr/bin/env python3

import os
import re
import io
import sys
import math
import logging
import argparse
import collections.abc

_log = logging.getLogger(__name__)
_FULL = '#'
_EMPTY = '.'


def _render_pots(pots):
    assert isinstance(pots, list) or isinstance(pots, tuple)
    return ''.join([_FULL if pot else _EMPTY for pot in pots])


class Base(object):

    def __init__(self, n, digifier=None):
        self.n = n
        self.digifier = digifier
        self.lenient = False
    
    def digify(self, symbol):
        if self.digifier:
            val = self.digifier(symbol)
        else:
            val = int(symbol)
        if not self.lenient and val >= self.n:
            raise ValueError("symbol is out of range for base {}".format(self.n))
        return val

    def bigendian(self, bits, nbits=None):
        value = 0
        if nbits is None:
            assert isinstance(bits, collections.abc.Sized), "if nbits is not specified, bit sequence must be a Sized collection"
            nbits = len(bits)
        i = 0
        for bit in bits:
            if bit:
                val = self.digify(bit)
                value += (val * (self.n ** (nbits - i - 1)))
            i += 1
        return value


BASE_TWO = Base(2)


class Rule(tuple):

    index, result, rendering = None, None, ''

    def __new__(cls, index, result):
        instance = super(Rule, cls).__new__(cls, [index, result])
        instance.index = index
        instance.result = result
        instance.rendering = instance.render()
        return instance
    
    def render(self, min_width=5):
        fmt_spec = "{0:0" + str(int(min_width)) + "b}"
        buckets = [bool(int(ch)) for ch in fmt_spec.format(self.index)]
        result_str = _FULL if self.result else _EMPTY
        return "{} => {}".format(_render_pots(buckets), result_str)
    
    @classmethod
    def parse(cls, line):
        m = re.fullmatch(r'^\s*([.#]+)\s*=>\s*([.#])\s*$', line)
        if m is None:
            raise ValueError("line does not match pattern: {}".format(line))
        index_str, result_str = m.group(1), m.group(2)
        bits = [ch == _FULL for ch in index_str]
        return Rule(BASE_TWO.bigendian(bits), result_str == _FULL)
    
    def __str__(self):
        return self.rendering
    
    @classmethod
    def find_max_width(cls, rules):
        max_index = max([rule.index for rule in rules])
        return int(math.log2(max_index)) + 1


def bit_generator(yielder, key_min, key_max_exclusive):
    for i in range(key_min, key_max_exclusive):
        yield yielder(i)


class State(object):

    def __init__(self, pots):
        self.plants = set([k for k in pots.keys() if pots[k]])
        keys = pots.keys()
        self.min_key = min(keys)
        self.max_key = max(keys)
    
    def render(self, from_key=None, to_key=None):
        if from_key is None:
            from_key = self.min_key
        if to_key is None:
            to_key = self.max_key
        buff = io.StringIO()
        for i in range(from_key, to_key + 1):
            buff.write(_FULL if self.is_full(i) else _EMPTY)
        return buff.getvalue()
    
    @classmethod
    def parse(cls, pots_str):
        pots_str = pots_str.strip()
        pots = {}
        for i in range(len(pots_str)):
            pots[i] = (pots_str[i] == _FULL)
        return State(pots)
    
    def is_full(self, pot_key):
        return pot_key in self.plants
    
    def _update_bounds(self, key, value):
        if value:
            if key < self.min_key:
                self.min_key = key
            if key > self.max_key:
                self.max_key = key
        else:
            self.min_key = min(self.plants)
            self.max_key = max(self.plants)
    
    def set_pot(self, key, value):
        if value:
            self.plants.add(key)
        else:
            self.plants.discard(key)
        self._update_bounds(key, value)
    
    def calc_index(self, pot_key, rule_width):
        key_min = pot_key - int(rule_width / 2)
        key_max_exclusive = key_min + rule_width
        nbits = key_max_exclusive - key_min
        bits = bit_generator(lambda i: self.is_full(i), key_min, key_max_exclusive)
        return BASE_TWO.bigendian(bits, nbits)
    
    def sum(self):
        pot_number_sum = 0
        for key in self.plants:
            pot_number_sum += key
        return pot_number_sum
    
    def capture(self):
        return frozenset(self.plants)
    
    def count(self):
        return len(self.plants)


def parse_state_and_rules(ifile=sys.stdin):
    state, rules = {}, []
    for line in ifile:
        if line.startswith("initial state: "):
            buckets = line[len("initial state: "):].strip()
            state = State.parse(buckets)
        else:
            line = line.strip()
            if line:
                rules.append(Rule.parse(line))
    return state, rules


class Processor(object):

    def __init__(self, rules, rule_width=None):
        if rule_width is None:
            rule_width = Rule.find_max_width(rules)
        assert rule_width > 0, "rule width must be positive integer"
        self.grow_rules = set()
        for rule in rules:
            if rule.index == 0:
                assert rule.result == False, "sequence of empty pots must not produce a plant"
            if rule.result:
                self.grow_rules.add(rule.index)
        self.grow_rules = frozenset(self.grow_rules)
        self.rule_width = rule_width
    
    def apply_rules(self, state, position):
        index = state.calc_index(position, self.rule_width)
        return index in self.grow_rules
    
    def process(self, state):
        assert isinstance(state, State)
        min_key = state.min_key - int(self.rule_width / 2)
        max_key = state.max_key + int(self.rule_width / 2) + 1
        updates = {}
        for position in range(min_key, max_key):
            update = self.apply_rules(state, position)
            if update is not None:
                updates[position] = update
        for key in updates:
            state.set_pot(key, updates[key])


def print_state(generation, state, args, always=False, ofile=sys.stdout):
    if always or args.very_verbose:
        current = state.render(args.render_min, args.render_max)
        print("{0:2d}: [{1:2d}] {2}".format(generation, state.min_key, current), file=ofile)
        return current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", default="/dev/stdin", help="input file", metavar="FILE")
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', metavar="LEVEL", help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    parser.add_argument("--rule-width", type=int, metavar="N", help="set rule width")
    parser.add_argument("--generations", type=int, metavar="N", default=20, help="max number of generations to iterate")
    parser.add_argument("--render-min", default=None, type=int)
    parser.add_argument("--render-max", default=None, type=int)
    parser.add_argument("--very-verbose", "--vv", action='store_true')
    parser.add_argument("--progress", type=int, metavar="N", help="report progress every N iterations")
    parser.add_argument("--final", action='store_true', help="print final state")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    _log.debug("reading from %s", args.input_file)
    with open(args.input_file, 'r') as ifile:
        state, rules = parse_state_and_rules(ifile)
    processor = Processor(rules, args.rule_width)
    for i in range(args.generations):
        print_state(i, state, args)
        processor.process(state)
        if args.progress and ((i + 1) % args.progress == 0):
            print("{} iterations performed, {} plants".format(i + 1, state.count()), file=sys.stderr)
    pot_number_sum = state.sum()
    print_state(i + 1, state, args, always=args.final)
    print("{} is the sum of the numbers of all pots ({}) that contain plants (min={})".format(pot_number_sum, state.count(), min(state.plants)))
    return 0

if __name__ == '__main__':
    exit(main())
