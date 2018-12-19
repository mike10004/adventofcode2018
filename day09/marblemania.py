#!/usr/bin/env python3

import sys
import io
import os
import logging
import argparse


_log = logging.getLogger(__name__)
MONEY = 23


def _NOOP(*args, **kwargs):
    pass


class Player(object):

    def __init__(self, tag):
        self._score = 0
        self.tag = tag

    def keep(self, marble):
        assert marble and isinstance(marble.n, int)
        self._score += marble.n
        return self._score
    
    def score(self):
        return self._score
    
    @classmethod
    def high_scorer(cls, players):
        high, scorer = None, None
        for player in players:
            score = player.score()
            if high is None or score > high:
                high = score
                scorer = player
        return scorer
    
    def __str__(self):
        return "[{}]".format(self.tag)
        


class Marble(object):

    def __init__(self, n, prev=None, next=None):
        self.n = n
        assert n is not None
        self.prev = prev or self
        self.next = next or self

    def __str__(self):
        prevn = None if self.prev is None else self.prev.n
        nextn = None if self.next is None else self.next.n
        return "Marble<{},prev={},next={}>".format(self.n, prevn, nextn)
    
    @classmethod
    def lowest(self, head):
        if head is None:
            return None
        if head.next is head:
            return head
        curr = head
        lowest = curr
        while True:
            if curr.n < lowest.n:
                lowest = curr
            assert curr is not curr.next, "loop at " + str(curr)
            curr = curr.next
            if curr is head:
                break
        return lowest
    
    def foreach(self, action, collect=False):
        curr = self
        items = []
        while True:
            retval = action(curr)
            if collect:
                items.append(retval)
            curr = curr.next
            if curr is self:
                break
        return items

    def advance(self, k):
        curr = self
        j = abs(k)
        for i in range(j):
            if k > 0:
                curr = curr.next
            else:
                curr = curr.prev
        return curr
    

class Circle(object):

    def __init__(self, curr=None):
        self.curr = curr or Marble(0)
        self.count = len(self.marbles())
    
    def marbles(self):
        return self.curr.foreach(lambda m: m, True)
    
    def render(self, ofile=sys.stdout):
        lowest = Marble.lowest(self.curr)
        if lowest is None:
            return
        def action(marble):
            val = str(marble.n)
            if marble is self.curr:
                val = "({})".format(val)
            print(val, end=" ", file=ofile)
        lowest.foreach(action)
    
    def rendering(self):
        buff = io.StringIO()
        self.render(buff)
        return buff.getvalue()
    
    def add(self, marble):
        insertion_pt = self.curr.next
        post_insertion_pt = insertion_pt.next
        post_insertion_pt.prev = marble
        insertion_pt.next = marble
        marble.prev = insertion_pt
        marble.next = post_insertion_pt
        self.curr = marble
        self.count += 1
    
    def remove(self, marble):
        assert marble.prev, "marble has no previous: " + str(marble)
        assert marble.next, "marble has no next: " + str(next)
        if self.count == 1:
            assert marble is self.curr, "tried to remove {} from circle containing only {}".format(marble, self.curr)
            self.curr = None
            return
        prev = marble.prev
        nxt = marble.next
        assert prev and nxt
        prev.next = nxt
        nxt.prev = prev
        self.curr = marble.next
        self.count -= 1
    
    @classmethod
    def construct(cls, values, current_value):
        assert values
        if len(values) == 1:
            return Circle(Marble(values[0]))
        marble = None
        first = None
        current = None
        for value in values:
            prev = marble
            marble = Marble(value)
            if first is None:
                first = marble
            marble.prev = prev
            if prev is not None:
                prev.next = marble
            if current_value == value:
                current = marble
        marble.next = first
        first.prev = marble
        assert current is not None, "current marble value not in list of values"
        return Circle(current)
    

class Game(object):

    def __init__(self, circle=None, state=None, moneyball=MONEY):
        self.circle = circle or Circle()
        self.state = state or 0
        self.moneyball = moneyball
    
    def step(self, player):
        self.state += 1
        marble = Marble(self.state)
        if marble.n % self.moneyball == 0:
            player.keep(marble)
            sevenccw = self.circle.curr.advance(-7)
            player.keep(sevenccw)
            self.circle.remove(sevenccw)
        else:
            self.circle.add(marble)
    
    def play(self, players, max_marble_value, callback=None):
        callback = callback or _NOOP
        nrounds = max_marble_value + 1
        while True:
            player = players[nrounds % len(players)]
            self.step(player)
            callback(player, self.circle)
            nrounds += 1
            if self.state >= max_marble_value:
                break
        return Player.high_scorer(players)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    with open(sys.stdin, 'r') as ifile:
        pass
    return 0

if __name__ == '__main__':
    exit(main())
