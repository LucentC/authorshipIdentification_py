#!/bin/bash

./preconfigure.sh ipost
service postgresql start
./preconfigure.sh ipost
./preconfigure.sh cdba
python -m flask run -p 80 -h 0.0.0.0
