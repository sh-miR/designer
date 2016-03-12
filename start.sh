#!/bin/bash

psql -U postgres -h db < /opt/shmir/shmirdesignercreate.sql
shmir-db-manage upgrade
shmir-db-seed

exec /usr/bin/uwsgi --http :8080 --module shmir --callable app
