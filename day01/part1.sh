#!/bin/bash

START="${START:-0}"
INPUT_FILE="${INPUT_FILE:-./input.txt}"

echo "${START}" | cat - "${INPUT_FILE}" | xargs | bc
