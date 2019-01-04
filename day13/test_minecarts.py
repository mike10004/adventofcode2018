#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
import minecarts

_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
    level = logging.__dict__.get(level_str, 'INFO')
    logging.basicConfig(level=level)
    _log.debug("logging configured at level %s (%s)", level, level_str)
    logging_configured = True


SAMPLE_TRACK_MAP_INPUT = """/->-\        
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/"""

class TestRender(unittest.TestCase):

    def test_render(self):
        lines = SAMPLE_TRACK_MAP_INPUT.split("\n")
        tracks, carts = minecarts.setup(lines)
        buffer = io.StringIO()
        minecarts.render(tracks, carts, range(13), range(6), buffer)
        actual = buffer.getvalue()
        self.assertEqual(SAMPLE_TRACK_MAP_INPUT, actual.strip())


class TestCrashPositionFinder(unittest.TestCase):

    def test_find_first_crash_position(self):
        lines = SAMPLE_TRACK_MAP_INPUT.split("\n")
        max_ticks = 50
        def callback(tracks, carts, nticks):
            # print(nticks)
            # minecarts.render(tracks, carts, range(15), range(7))
            self.assertLess(nticks, max_ticks, "breached max ticks threshold")
        tracks, carts = minecarts.setup(lines)
        position = minecarts.find_first_crash_position(tracks, carts, callback)
        self.assertEqual((7, 3), position)
        

class TestLastCartPositionFinder(unittest.TestCase):

    def test_find_last_cart_position(self):
        lines = [
            '/>-<\\  ', 
            '|   |  ', 
            '| /<+-\\', 
            '| | | v', 
            '\\>+</ |', 
            '  |   ^', 
            '  \\<->/']
        tracks, carts = minecarts.setup(lines)
        position = minecarts.find_last_cart_position(tracks, carts)
        self.assertEqual((6, 4), position)