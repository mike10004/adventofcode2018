#!/bin/bash

set -e

INPUT_FILE=$1

if [ -z "$INPUT_FILE" ] ; then
    echo "exactly one argument, the input file, must be provided" >&2
    exit 1
fi

TABLE=""

for UNITS in aA bB cC dD eE fF gG hH iI jJ kK lL mM nN oO pP qQ rR sS tT uU vV wW xX yY zZ; do   
    echo -n "${UNITS}: "
    REACTED_CHARS=$(sed "s/[$UNITS]//g" "$INPUT_FILE" | bin/polymers | wc -m)
    REACTED_CHARS=$(echo $REACTED_CHARS - 1 | bc)
    echo -ne "\t$REACTED_CHARS\n"
    TABLE=$(echo -en "${TABLE}\n${REACTED_CHARS}\t${UNITS}\n")
done

echo "$TABLE" | sort -n -k1 | head -n2

