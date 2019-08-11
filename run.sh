#!/bin/bash

IMGNAME=author-stylometry-pack
LOCALPORT=8080
#VOL="-v /pgdata/:/var/lib/postgresql/10/main -v /postgres/:/postgres/"
VOL="-v /Users/schent/Garage/playground/demo:/postgres/"

docker build -t $IMGNAME .
docker run -ti --restart=always -p $LOCALPORT:80 $VOL $IMGNAME 

