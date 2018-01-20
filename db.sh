#!/bin/bash
#
#
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib libz-dev libjpeg-dev libfreetype6-dev python-dev

echo "CREATE DATABASE django_boards; \
CREATE USER django_boards WITH PASSWORD 'django_boards'; \
ALTER ROLE django_boards SET client_encoding TO 'utf8'; \
ALTER ROLE django_boards SET timezone TO 'UTC'; \
GRANT ALL PRIVILEGES ON DATABASE django_boards TO django_boards;" | sudo su postgres -c psql
