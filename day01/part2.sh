#!/bin/bash

START="${START:-0}"
INPUT_FILE="${INPUT_FILE:-./input.txt}"

SUM="${START}"
DELIM="\n"
SEEN="${SUM}${DELIM}"

while true; do
    echo "reading from ${INPUT_FILE}" >&2
    while read LINE; do
        SUM=$(echo "${SUM} ${LINE}" | bc)
        COUNT=$(echo -e "${SEEN}" | grep --count --max-count=1 --regexp="^$SUM$")
        if [ $COUNT -ne 0 ] ; then
          echo "duplicate: $SUM"
          exit 0
        fi
        SEEN="${SEEN}${SUM}${DELIM}"
    done < "${INPUT_FILE}"
done
