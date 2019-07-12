#!/bin/bash

PARMDBUSER="postgres"
PARMNEWDBUSER="stylometry"
PARMNEWDBPW=$PARMNEWDBUSER
PARMNEWDBNAME=$PARMNEWDBUSER

PARMPATHTOSQL="database_sql_files"
PARMPOSTGRESQL="postgresql postgresql-contrib"
PARMAPTPACK="python-nltk python-psycopg2 python-flask python-numpy python-scipy python-sklearn python-scrapy"

function install_py_packages
{
    apt-get install $PARMAPTPACK -y
}

function create_database
{
    # apt-get install $PARMPOSTGRESQL -y
    useradd -s /bin/bash -m $PARMNEWDBUSER
    su - $PARMDBUSER -c "psql -c \"CREATE USER $PARMNEWDBUSER WITH PASSWORD '$PARMNEWDBPW';\""
    su - $PARMDBUSER -c "psql -c \"CREATE DATABASE $PARMNEWDBNAME;\""
    su - $PARMDBUSER -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $PARMNEWDBNAME TO $PARMNEWDBUSER;\""
}

function create_author_doc_tables
{
    su - $PARMNEWDBUSER -c "psql -f \"$(pwd)\"/$PARMPATHTOSQL/create_author_doc_tables.sql"
}

function create_other_tables
{
    su - $PARMNEWDBUSER -c "psql -f \"$(pwd)\"/$PARMPATHTOSQL/create_other_tables.sql"
}

function create_all_tables
{
    create_author_doc_tables
    create_other_tables
}

function drop_other_tables
{
    su - $PARMNEWDBUSER -c "psql -f \"$(pwd)\"/$PARMPATHTOSQL/drop_other_tables.sql"
}

function drop_all_tables
{
    drop_other_tables
    su - $PARMNEWDBUSER -c "psql -f \"$(pwd)\"/$PARMPATHTOSQL/drop_author_doc_tables.sql"
}

function insert_features
{
    su - $PARMNEWDBUSER -c "psql -f \"$(pwd)\"/$PARMPATHTOSQL/insert_features.sql"
}

function print_usage
{
    echo -e "Usage: $0 [ipy|ipost|cdbad|cdbo]"
    echo -e "\tipy - install required python packages"
    echo -e "\tipost - install postgresql and create user"
    echo -e "\tcdbad - create author and document tables"
    echo -e "\tcdbo - create other tables"
    echo -e "\tcdba - create all tables"
    echo -e "inf - insert feature details"
    echo -e "\tdot - drop other tables"
    echo -e "\tdat - drop all tables"
}

if [ $# != 1 ];then
    print_usage
    exit 1
fi

if [ "$(whoami)" != "root" ];then
    echo "$0 must be run as root."
    exit 1
fi

case "$1" in
    "ipy")      install_py_packages ;;
    "ipost")    create_database ;;
    "cdbad")    create_author_doc_tables ;;
    "cdbo")     create_other_tables ;;
    "cdba")     create_all_tables ;;
    "inf")      insert_features ;;
    "dot")      drop_other_tables ;;
    "dat")      drop_all_tables ;;
    *)          print_usage ;;
esac