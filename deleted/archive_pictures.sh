#!/bin/bash

MODE="lp"

if [ $# -ge 1 ]
then
    MODE=$1
fi

grep -o "original_pic\": \"[^\"]*\"" ${MODE}.json | cut -d\" -f3 | sort -u > ${MODE}.pictures.txt
grep -o "thumbnail_pic\": \"[^\"]*\"" ${MODE}.json | cut -d\" -f3 | sort -u > ${MODE}.pictures.thumb.txt

cd pictures

cd original
while read i
do
    F=`echo $i | cut -d\/ -f5`
    if [ `ls ${F} 2> /dev/null | wc -l ` -ge 1 ]
    then
        continue
    fi
    curl -s $i -o ${F}
done < ../../${MODE}.pictures.txt
cd ..

cd thumbnail
while read i
do
    F=`echo $i | cut -d\/ -f5`
    if [ `ls ${F} 2> /dev/null | wc -l ` -ge 1 ]
    then
        continue
    fi
    curl -s $i -o ${F}
done < ../../${MODE}.pictures.thumb.txt
cd ..

cd ..

rm ${MODE}.pictures.txt
rm ${MODE}.pictures.thumb.txt
