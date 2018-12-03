#!/usr/bin/python3

import sys
from argparse import ArgumentParser

def examine(sequence, collection_type=set, max_attempts=128000):
    already_seen = collection_type()
    sum_ = 0
    num_attempts = 0
    while num_attempts < max_attempts:
        for number in sequence:
            sum_ += number
            if sum_ in already_seen:
                return sum_ 
            already_seen.add(sum_)
        num_attempts += 1
    return None

def main():
    parser = ArgumentParser()
    parser.add_argument("input_file", default="/dev/stdin")
    args = parser.parse_args()
    if args.input_file == '-':
        args.input_file = "/dev/stdin"
    with open(args.input_file, 'r') as ifile:
        sequence = [line.strip() for line in ifile]
    sequence = map(lambda line: line.lstrip('+'), sequence)
    sequence = map(int, sequence)
    found = examine(list(sequence))
    if found is not None:
        print("duplicate:", found)
        return 0 
    else:
        print("no duplicate encountered", file=sys.stderr)
        return 2

if __name__ == '__main__':
    exit(main())