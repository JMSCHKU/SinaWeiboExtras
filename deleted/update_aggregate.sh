#!/bin/bash

D=`date +%Y%m%d-%H%M`
MODE="lp"

if [ $# -ge 1 ]
then
    MODE=$1
fi

curl -s "http://research.jmsc.hku.hk/social/sinaweibo/${MODE}.json" -o ${MODE}.${D}.json

./update_aggregate.py ${MODE}.json ${MODE}.${D}.json > ${MODE}.new.json

if [ `wc -m ${MODE}.new.json | cut -d" " -f1` -gt 100000 ]
then
    mv ${MODE}.new.json ${MODE}.json
fi

if [ ${MODE} == "lp" ]
then
    ./translate_weibos.py ${MODE}.json > ${MODE}.translation.json
    if [ `wc -m ${MODE}.translation.json | cut -d" " -f1` -gt 100000 ]
    then
        mv ${MODE}.translation.json ${MODE}.json
    fi
fi

mv ${MODE}.${D}.json archive
