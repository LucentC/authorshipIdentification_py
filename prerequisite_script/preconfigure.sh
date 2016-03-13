#!/bin/bash

PARMAPTPACK="python-nltk python-psycopg2 python-flask python-numpy python-scipy python-sklearn python-scrapy"

function install_py_packages
{
    apt-get install $PARMAPTPACK -y
}

function create_database
{

}


if [ "$(whoami)" != "root" ];then
    echo "$0 must be run as root."
    exit 1
fi