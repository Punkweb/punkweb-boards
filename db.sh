#!/bin/bash

echo "CREATE DATABASE punkweb_boards; \
CREATE USER punkweb_boards WITH PASSWORD 'punkweb_boards'; \
ALTER ROLE punkweb_boards SET client_encoding TO 'utf8'; \
ALTER ROLE punkweb_boards SET timezone TO 'UTC'; \
GRANT ALL PRIVILEGES ON DATABASE punkweb_boards TO punkweb_boards;" | sudo su postgres -c psql