#!/bin/bash

IMGNAME=stylometry_web
NAME=stylometry_web
LOCALPORT=16112
VOL="-v /postgres/demo/stylometry_demo.sql:/postgres/stylometry.sql"

if [[ "$(docker images -q $IMGNAME 2> /dev/null)" == "" ]]; then
  docker build -t $IMGNAME .;
fi

echo $VOL
docker run --name $NAME -d --restart=always -e FLASK_DEBUG=1 -p $LOCALPORT:80 $VOL $IMGNAME bash -c \
  "service postgresql start && \
  ./preconfigure.sh ipost && \
  su stylometry -c \"psql -d stylometry -f /postgres/stylometry.sql\" && \
  su postgres -c \"psql -d stylometry -c 'create extension tablefunc;'\" && \
  python -m flask run -p 80 -h 0.0.0.0"


