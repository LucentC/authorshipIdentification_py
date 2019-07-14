#!/bin/bash

IMGNAME=author-stylometry-pack
LOCALPORT=8080
VOL="-v /pgdata/:/var/lib/postgresql/10/main -v /postgres/:/postgres/"

docker build -t $IMGNAME .
docker run -d --restart=always -p $LOCALPORT:80 $IMGNAME 

