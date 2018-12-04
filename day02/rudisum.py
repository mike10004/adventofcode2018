#!/usr/bin/env python3

import sys
import argparse
from collections import defaultdict


class RepeatCharPredicate(object):

    def __init__(self):
        pass
    
    def count(self, sequence):
        counts = defaultdict(lambda: 0)
        for ch in sequence:
            counts[ch] = counts[ch] + 1
        return counts
    
    def evaluate(self, sequence, required_count):
        counts = self.count(sequence)
        return ''.join(filter(lambda ch: counts[ch] == required_count, counts.keys()))


def compute_checksum(sequences, counts):
    checksum_factors = defaultdict(lambda: 0)
    predicate = RepeatCharPredicate()
    for required_count in counts:
        for sequence in sequences:
            matches = predicate.evaluate(sequence, required_count)
            checksum_factors[required_count] += (1 if matches else 0)
    checksum = 1
    for factor in checksum_factors.values():
        checksum *= factor
    return checksum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", default="/dev/stdin")
    parser.add_argument("--counts", nargs='+', default=(2, 3,))
    args = parser.parse_args()
    with open(args.input, 'r') as ifile:
        sequences = [s.strip() for s in ifile]
    checksum = compute_checksum(sequences, args.counts)
    print(checksum)
    return 0

if __name__ == '__main__':
    exit(main())
