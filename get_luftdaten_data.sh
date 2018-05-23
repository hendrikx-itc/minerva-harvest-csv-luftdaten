#!/bin/bash

if [ -d "/data/trendstore" ]; then
    if [ ! -f "/tmp/trendstoredone" ]; then
        /plugins/aireas/setup_trendstore.sh
    fi
fi

rm -r $DIRNAME/`/plugins/csv/getdate.py 8`

DIRNAME=$1
mkdir -p $1

DATE="none"

for DAYSAGO in 1 2 3 4 5 6 7
do
   PREDATE=`/plugins/csv/getdate.py $DAYSAGO`
   if [ ! -f "$DIRNAME/$PREDATE.done" ]; then
      DATE=$PREDATE
   fi
done

if [ $DATE != none ]
then
    mkdir -p $DIRNAME/$DATE
    /plugins/csv/loadallcsv.py "http://archive.luftdaten.info/$DATE/" $DIRNAME/$DATE
    touch "$DIRNAME/$DATE.done"

    for i in $DIRNAME/$DATE/*
    do
        echo "Doing $i"
        PGDATABASE=minerva PGHOST=database PGUSER=postgres /usr/local/bin/minerva load-data --data-source luftdaten -p csv -v --statistics $i
    done
fi
