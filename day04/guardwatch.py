#!/usr/bin/env python3

import sys
import re

from collections import defaultdict

MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = MINUTES_PER_HOUR * 24

class Time(tuple):

    year = None
    month = None
    day = None
    hour = None
    minute = None

    def __new__(cls, year, month, day, hour, minute):
        me = super(Time, cls).__new__(cls, tuple([year, month, day, hour, minute]))
        me.hour = hour
        me.minute = minute
        me.year = year
        me.month = month
        me.day = day
        return me
    
    @classmethod
    def parse(cls, line):
        m = re.fullmatch(r'^\[(\d+)-0?(\d+)-0?(\d+)\s0?(\d+):0?(\d+)\]\s+.*$', line.strip())
        assert m is not None, "line does not match pattern: " + repr(line)
        year, month, day, hour, minute = [int(m.group(i)) for i in range(1, 6)]
        return Time(year, month, day, hour, minute)
    
    def since(self, then):
        """Calculates minutes between the argument Time and this time."""
        diff = [self[i] - then[i] for i in range(len(then))]
        assert diff[0] == 0 and diff[1] == 0, "can't calculate minutes across months or years: " + str([self, then])
        minutes = diff[2] * MINUTES_PER_DAY + diff[3] * MINUTES_PER_HOUR + diff[4]
        return minutes



class Shift(tuple):

    guard_id = None
    events = tuple()

    def __new__(cls, guard_id, events):
        """Constructs a new shift object.
        Events is a list of Time objects representing [shift starts, falls asleep, wakes up, ...].
        """
        assert len(events) > 0, "expect at least one event in shift"
        if len(events) % 2 == 0:
            # add an event representing waking up at the end of the shift (01:00)
            last = events[-1]
            events.append(Time(last.year, last.month, last.day, 1, 0))
        events = tuple(events)
        me = super(Shift, cls).__new__(cls, tuple([guard_id, events]))
        me.guard_id = guard_id
        me.events = events
        return me
    
    def list_minutes_asleep(self):
        minutes = []
        for i in range(1, len(self.events)):
            if i % 2 == 0:
                falls_asleep = self.events[i - 1]
                wakes_up = self.events[i]
                minutes += list(range(falls_asleep.minute, wakes_up.minute))
        return minutes
    
    def count_minutes_asleep(self):
        total = 0
        for i in range(1, len(self.events)):
            if i % 2 == 0:
                falls_asleep = self.events[i - 1]
                wakes_up = self.events[i]
                duration = wakes_up.since(falls_asleep)
                total += duration
        return total
    
    def is_asleep_at_minute(self, minute):
        return minute in self.list_minutes_asleep()


class ShiftParser(object):

    def parse(self, lines):
        event_lines = {}
        for line in lines:
            if not line:
                continue
            event_time = Time.parse(line)
            event_lines[event_time] = line
        shifts = []
        guard_id = None
        events = []
        event_times = sorted(event_lines.keys())
        for event_time in event_times:
            line = event_lines[event_time]
            if not line:
                continue
            event_time = Time.parse(line)
            if 'Guard' in line:
                if guard_id is not None:
                    shift = Shift(guard_id, events)
                    events = []
                    shifts.append(shift)
                m = re.search("Guard\s+#(\d+)\s+", line)
                assert m is not None, "line does not match pattern: " + line
                guard_id = m.group(1)
            events.append(event_time)
        if guard_id is not None:
            shift = Shift(guard_id, events)
            events = []
            shifts.append(shift)
        return shifts


def print_minute_histo(histo):
    for minute in sorted(histo.keys()):
        count = histo[minute]
        print("%02d %s" % (minute, count))


def argmax(scriptable, keys):
    mx = None
    a = None
    for key in keys:
        curr = scriptable[key]
        if mx is None or curr > mx:
            mx = curr
            a = key
    return a, mx

def compute_stuff():
    lines = [line for line in sys.stdin]
    shifts = ShiftParser().parse(lines)
    shifts_by_guard = defaultdict(list)
    sleep_counts = defaultdict(int)
    sleepiest_guard, most_minutes_slept = None, -1
    for shift in shifts:
        shifts_by_guard[shift.guard_id].append(shift)
        minutes = shift.count_minutes_asleep()
        sleep_counts[shift.guard_id] += minutes
        if sleep_counts[shift.guard_id] > most_minutes_slept:
            sleepiest_guard = shift.guard_id
            most_minutes_slept = sleep_counts[shift.guard_id]
    print("sleepest guard is {} ({} minutes)".format(sleepiest_guard, sleep_counts[sleepiest_guard]))
    histo = defaultdict(int)
    for shift in shifts_by_guard[sleepiest_guard]:
        minutes = shift.list_minutes_asleep()
        for minute in minutes:
            histo[minute] += 1
    print_minute_histo(histo)
    sleepage = defaultdict(list)
    for minute in range(MINUTES_PER_HOUR):
        for shift in shifts:
            if shift.is_asleep_at_minute(minute):
                sleepage[minute].append(shift.guard_id)
    # histo is map of minute -> guard_count
    # guard_count is map of guard_id -> number of shifts for guard was asleep at that minute
    histo = {}  
    for minute, guard_ids in sleepage.items():
        guard_count = defaultdict(int)
        for guard_id in guard_ids:
            guard_count[guard_id] += 1
        histo[minute] = guard_count
    print()
    print("minute / sleepiest / # sleeps")
    for minute in sorted(histo.keys()):
        guard_count = histo[minute]
        sleepiest_at_minute, count = argmax(guard_count, guard_count.keys())
        print("%02d guard %4s %d" % (minute, sleepiest_at_minute, count))
    return 0


def main():
    compute_stuff()
    return 0


if __name__ == '__main__':
    exit(main())
