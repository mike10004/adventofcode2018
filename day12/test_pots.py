#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from pots import Rule, State, Processor

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
        
