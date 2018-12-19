#!/usr/bin/env python3

import os
import sys
import unittest
import io
import marblemania
import logging
from marblemania import Circle, Marble, Player, Game


_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
    level = logging.__dict__.get(level_str, 'INFO')
    logging.basicConfig(level=level)
    print("\n", file=sys.stderr)
    _log.debug("logging configured at level %s (%s)", level, level_str)
    logging_configured = True


class TestMarble(unittest.TestCase):

    def test_nothing(self):
        _log.debug("hello, world")


class TestCircle(unittest.TestCase):

    def test_construct(self):
        circle = Circle.construct([0, 8, 4,  2,  5,  1,  6,  3,  7], 8)
        expected = "0 (8) 4  2  5  1  6  3  7"
        self.assertListEqual(expected.split(), circle.rendering().split())
    
    def test_construct2(self):
        circle = Circle.construct([2, 5, 8], 8)
        self.assertEqual(3, len(circle.marbles()))
        def has_neighbors(m):
            self.assertIsNotNone(m.prev, "prev is None on " + str(m))
            self.assertIsNotNone(m.next, "next is None on " + str(m))
        circle.curr.foreach(has_neighbors)
    
    def test_remove_current(self):
        circle = Circle.construct([2, 5, 8], 5)
        middle = circle.curr
        circle.remove(middle)
        self.assertEquals(8, circle.curr.n)
        self.assertEquals(2, circle.curr.prev.n)
        self.assertEquals(2, circle.curr.next.n)
        self.assertEqual(2, circle.count)

    def test_remove_other(self):
        circle = Circle.construct([2, 5, 8], 8)
        left = circle.curr.next
        assert left is not circle.curr
        assert left.n == 2
        circle.remove(left)
        self.assertEqual(5, circle.curr.n)
        self.assertEqual(8, circle.curr.prev.n)
        self.assertEqual(8, circle.curr.next.n)
        self.assertEqual(2, circle.count)
    
    def test_add(self):
        circle = Circle()
        self.assertEqual(1, circle.count)
        zero = circle.curr
        one = Marble(1)
        circle.add(one)
        self.assertEqual(2, circle.count)
        self.assertIs(circle.curr, one)
        self.assertIs(one.prev, zero)
        self.assertIs(one.next, zero)
        self.assertIs(zero.prev, one)
        self.assertIs(zero.next, one)
        two = Marble(2)
        circle.add(two)
        self.assertEqual(3, circle.count)
        self.assertIs(circle.curr, two)
        self.assertIs(one.prev, two)
        self.assertIs(one.next, zero)
        self.assertIs(zero.prev, one)
        self.assertIs(zero.next, two)
        self.assertIs(two.prev, zero)
        self.assertIs(two.next, one)



class TestGame(unittest.TestCase):

    def test_step_money(self):
        values = list(map(int, "0 16  8 17  4 18  9 19  2 20 10 21  5 22 11  1 12  6 13  3 14  7 15".split()))
        circle = Circle.construct(values, 22)
        game = Game(circle, 22)
        player = Player(5)
        game.step(player)
        actual = game.circle.rendering().split()
        expected = "0 16  8 17  4 18 (19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15".split()
        self.assertListEqual(expected, actual)

    def test_play(self):
        nelves = 9
        rounds = 25
        game = Game()
        players = [Player(i + 1) for i in range(nelves)]
        high_scorer = game.play(players, 25)
        self.assertEqual(25, game.circle.curr.n)
        self.assertEqual(32, high_scorer.score())

    
    def test_play_samples(self):
        max_cases = None
        test_cases = [
            (10, 1618, 8317),
            (13, 7999, 146373),
            (17, 1104, 2764),
            (21, 6111, 54718),
            (30, 5807, 37305),
        ]
        for nelves, last_marble_n, high_score in test_cases[:max_cases]:
            def enforce_limit(p, c): 
                if p.score() > high_score:
                    raise AssertionError("failure: score {} too high for player {}".format(p.score(), p))
            with self.subTest():
                players = [Player(i + 1) for i in range(nelves)]
                game = Game()
                high_scorer = game.play(players, last_marble_n, enforce_limit)
                actual_high_score = high_scorer.score()
                _log.debug("%s elves up to marble %s: expect high score %s, actual %s", nelves, last_marble_n, high_score, actual_high_score)
                self.assertEqual(high_score, actual_high_score, "{} elves high score".format(nelves))
    

