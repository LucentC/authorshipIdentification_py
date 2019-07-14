#!/bin/bash

./preconfigure.sh ipost
service postgresql start
./preconfigure.sh ipost
sleep 10;
./preconfigure.sh cdba
sleep 5;
python -m flask run -p 80 -h 0.0.0.0
