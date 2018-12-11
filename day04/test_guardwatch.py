#!/usr/bin/env python3

import unittest
from guardwatch import Time, Shift, ShiftParser

class TestTime(unittest.TestCase):

    def test_parse(self):
        t = Time.parse('[1518-11-01 00:05] falls asleep')
        self.assertEqual(Time(1518, 11, 1, 0, 5), t)
        t = Time.parse('[1518-11-01 00:00] Guard #10 begins shift\n')
        self.assertEqual(Time(1518, 11, 1, 0, 0), t)
    
    def test_since(self):
        now = Time(1518, 11, 1, 0, 25)
        then = Time(1518, 11, 1, 0, 5)
        self.assertEqual(20, now.since(then))
        now = Time(1518, 11, 2, 0, 40)
        then = Time(1518, 11, 1, 23, 58)
        self.assertEqual(42, now.since(then))
        # now, then = (1518, 10, 14, 0, 0), (1518, 9, 25, 0, 28)
        # self.assertEqual()


class TestShiftParser(unittest.TestCase):

    def test_parse(self):
        text = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""
        lines = text.split("\n")
        shifts = ShiftParser().parse(lines)
        self.assertEqual(5, len(shifts))
        first = shifts[0]
        self.assertEqual(first.guard_id, '10')
        self.assertEqual(len(first.events), 5)
        last = shifts[-1]
        self.assertEqual(last.guard_id, '99')
        self.assertEqual(len(last.events), 3)