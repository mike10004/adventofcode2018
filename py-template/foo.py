#!/usr/bin/env python3

import sys
import os
import logging
import argparse


_log = logging.getLogger(__name__)


class Tupleish(tuple):

    a, b = None, None

    def __new__(cls, a, b):
        instance = super(Tupleish, cls).__new__(cls, [a, b])
        instance.a = a
        instance.b = b
        return instance


class Processor(object):

    def __init__(self):
        pass
    
    def process(self):
        pass
    

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
