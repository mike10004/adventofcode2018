#!/usr/bin/env python3

import argparse

_ZERO_CHAR = 0

def compute_charwise_distances(a, b):
    a, b = [c for c in a], [c for c in b]
    # make arrays congruent
    a = a + ([_ZERO_CHAR] * max(0, len(b) - len(a)))
    b = b + ([_ZERO_CHAR] * max(0, len(a) - len(b)))
    assert len(a) == len(b)
    return [ord(a[i]) - ord(b[i]) for i in range(len(a))]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", default="/dev/stdin")
    args = parser.parse_args()
    with open(args.input, 'r') as ifile:
        sequences = [s.strip() for s in ifile]
    distances = find_distances(sequences)
    for k, ds in distances.items():
        if len(list(filter(lambda x: x != 0, ds))) == 1:
            print(k)
    return 0

def find_distances(sequences):
    distances = {}
    for i in range(0, len(sequences)):
        for j in range(i + 1, len(sequences)):
            a, b = sequences[i], sequences[j]
            distances[(a, b)] = compute_charwise_distances(a, b)
    return distances

if __name__ == '__main__':
    exit(main())
