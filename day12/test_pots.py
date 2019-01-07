#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from pots import Base, Rule, State, Processor

_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
    level = logging.__dict__.get(level_str, 'INFO')
    logging.basicConfig(level=level)
    _log.debug("logging configured at level %s (%s)", level, level_str)
    logging_configured = True


_RULE_INPUT_TEST_CASES = [            
    ('.#.## => #', 11, True),
    ('....# => #', 1, True),
    ('...#. => .', 2, False),
    ('#.... => #', 16, True),
    ('.#### => .', 15, False),
]


def load_sample_rules():
    rules_str = [
        "...## => #",
        "..#.. => #",
        ".#... => #",
        ".#.#. => #",
        ".#.## => #",
        ".##.. => #",
        ".#### => #",
        "#.#.# => #",
        "#.### => #",
        "##.#. => #",
        "##.## => #",
        "###.. => #",
        "###.# => #",
        "####. => #",
    ]
    sample_rules = [Rule.parse(rule_str) for rule_str in rules_str]
    return frozenset(sample_rules)


class TestRule(unittest.TestCase):

    def test_parse(self):
        for rule_str, index, result in _RULE_INPUT_TEST_CASES:
            with self.subTest():
                rule = Rule.parse(rule_str)
                self.assertEqual(index, rule.index)
                self.assertEqual(result, rule.result)
    
    def test_render(self):
        for expected, index, result in _RULE_INPUT_TEST_CASES:
            with self.subTest():
                rule = Rule(index, result)
                actual = rule.render()
                self.assertEqual(expected, actual)
    
    def test_find_max_width(self):
        rules = [Rule.parse(rule_str) for rule_str, index, result in _RULE_INPUT_TEST_CASES]
        max_width = Rule.find_max_width(rules)
        self.assertEqual(5, max_width)


class TestState(unittest.TestCase):

    def test_parse(self):
        state = State.parse("#..#.#..##......###...###")
        self.assertTrue(state.is_full(0))
        self.assertTrue(state.is_full(3))
        self.assertTrue(state.is_full(5))
        self.assertFalse(state.is_full(1))
        self.assertFalse(state.is_full(2))
        self.assertFalse(state.is_full(4))

    def test_render(self):
        state = State.parse("#..#.#..##......###...###")
        rendering = state.render(-3)
        self.assertEqual("...#..#.#..##......###...###", rendering)
    
    def test_calc_index(self):
        state = State.parse("#..#.#..##......###...###")
        test_cases = [
            (0, 5, 4),
            (2, 5, 18),
            (20, 5, 17),
        ]
        for key, rule_width, expected in test_cases:
            with self.subTest():
                self.assertEqual(expected, state.calc_index(key, rule_width))


class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.sample_rules = load_sample_rules()
        print(file=sys.stderr)
    
    def test_apply_rules(self):
        state = State.parse("#..#.#..##......###...###")
        processor = Processor(self.sample_rules, 5)
        test_cases = [
            (4, True),
            (22, False),
        ]
        for position, expected in test_cases:
            with self.subTest():
                actual = processor.apply_rules(state, position)
                self.assertEqual(expected, actual)

    def test_apply_rules_2(self):
        state = State.parse("#...#....#.....#..#..#..#")
        processor = Processor(self.sample_rules, 5)
        self.assertEqual(True, processor.apply_rules(state, 1))

    def test_process(self):
        test_cases = [
            (0,  "...#..#.#..##......###...###..........."),
            (1,  "...#...#....#.....#..#..#..#..........."),
            (2,  "...##..##...##....#..#..#..##.........."),
            (5,  "....#...##...#.#..#..#...#...#........."),
            (10, "..#.#..#...#.##....##..##..##..##......"),
            (20, ".#....##....#####...#######....#.#..##."),
        ]
        processor = Processor(self.sample_rules, 5)
        from_key, to_key = -3, 35
        for generations, rendering in test_cases:
            state = State.parse("#..#.#..##......###...###")
            with self.subTest():
                for i in range(generations):
                    before = state.render(from_key, to_key)
                    _log.debug("[%s] before processing: %s", i, before)
                    processor.process(state)
                    after = state.render(from_key, to_key)
                    _log.debug("[%s]  after processing: %s", i, after)
                actual = state.render(from_key, to_key)
                self.assertEqual(rendering, actual, "after {} generations".format(generations))
        

def sequence_to_generator(seq):
    for element in seq:
        yield element


class TestBase(unittest.TestCase):

    def do_test_bigendian(self, n, test_cases):
        std_cases = [
            (0, tuple()),
            (0, (False,)),
            (0, (False, False, False,)),
        ]
        base = Base(n)
        for expected, bits in test_cases:
            original = list(bits)
            nbits = len(bits)
            with self.subTest():
                self.assertEqual(expected, base.bigendian(bits), "expect {} == {}".format(bits, expected))
            with self.subTest():
                bits = sequence_to_generator(bits)
                self.assertEqual(expected, base.bigendian(bits, nbits), "(generator) expect {} == {}".format(original, expected))

    def test_base2_bigendian(self):
        test_cases = [
            (1, (True,)),
            (1, (False, True,)),
            (2, (True, False,)),
            (3, (True, True,)),
            (4, (True, False, False)),
            (4, (False, True, False, False)),
            (4, (False, False, True, False, False)),
            (5, (False, False, True, False, True)),
        ]
        self.do_test_bigendian(2, test_cases)
    
    def test_base10_bigendian(self):
        test_cases = [
            (1, (1,)),
            (1, (0, 1,)),
            (1, (0, 0, 1,)),
            (3, (3,)),
            (12, (1, 2)),
            (12, (0, 1, 2)),
            (543, (5, 4, 3)),
            (1400, (1, 4, 0, 0)),
        ]
        self.do_test_bigendian(10, test_cases)
    
    def test_base16_bigendian(self):
        test_cases = [
            (1, (1,)),
            (1, (0, 1)),
            (4, (0, 4)),
            (10, (10,)),
            (15, (15,)),
            (15, (0, 15,)),
            (16, (1, 0)),
            (17, (1, 1)),
            (3 * 256 + 2 * 16 + 1 * 1, (3, 2, 1)),
        ]
        self.do_test_bigendian(16, test_cases)
    
    def test_base2_outofrange(self):
        try:
            Base(2).bigendian((2, 1, 0))
            self.fail("should have thrown exception")
        except ValueError:
            pass
