#!/bin/bash

set -e

sudo chown -R shmir: /var/lib/shmir/mfold
sudo chown -R shmir: /var/lib/shmir/blast
sudo chown -R shmir: /var/lib/shmir/bio_databases

exec $@
