#!/bin/bash

MODE="lp"

if [ $# -ge 1 ]
then
    MODE=$1
fi

./extract_text.py ${MODE}.json > ${MODE}.text.txt

while read line
do
    echo "${line}" | bamboo
done < ${MODE}.text.txt

#rm ${MODE}.text.txt
