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


class TestSolveA(unittest.TestCase):

    def test_solve_a(self):
        lines = """/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.split("\n")
        position = minecarts.solve_a(lines)
        print(position)
        

