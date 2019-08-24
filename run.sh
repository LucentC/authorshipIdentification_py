#!/bin/bash

IMGNAME=stylometry_web
LOCALPORT=16112
VOL="-v /postgres/demo/stylometry_demo.sql:/postgres/stylometry_demo.sql"

if [[ "$(docker images -q $IMGNAME 2> /dev/null)" == "" ]]; then
  docker build -t $IMGNAME .;
fi

echo $VOL
docker run -d --restart=always -e FLASK_DEBUG=1 -p $LOCALPORT:80 $VOL $IMGNAME bash -c \
  "service postgresql start && \
  ./preconfigure.sh ipost && \
  su stylometry -c \"psql -d stylometry -f /postgres/stylometry.sql\" && \
  python -m flask run -p 80 -h 0.0.0.0"

# restore data
# su stylometry -c "psql -d stylometry -f /postgres/stylometry.sql"
# python -m flask run -p 80 -h 0.0.0.0

