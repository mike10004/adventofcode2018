#!/bin/bash

set -e

INPUT_FILE="${1:-input.txt}"
OUTPUT_FILE="${2:-/dev/null}"  # use /dev/stdout to print output string
gcc -o bin/polymers polymers.c

bin/polymers < "${INPUT_FILE}" > /dev/null
