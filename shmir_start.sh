#!/bin/bash

set -e

sudo chown -R shmir: /var/lib/shmir/mfold
sudo chown -R shmir: /var/lib/shmir/blast
sudo chown -R shmir: /var/lib/shmir/bio_databases

psql -U postgres -h db < /opt/shmir/shmirdesignercreate.sql
shmir-db-manage upgrade
shmir-db-seed

exec /usr/bin/uwsgi --http :8080 --module shmir --callable app
