#!/bin/bash

sudo chown -R shmir: /tmp/mfold_files
sudo chown -R shmir: /opt/shmir/databases

psql -U postgres -h db < /opt/shmir/shmirdesignercreate.sql
shmir-db-manage upgrade
shmir-db-seed

exec /usr/bin/uwsgi --http :8080 --module shmir --callable app
