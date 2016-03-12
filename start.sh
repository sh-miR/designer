#!/bin/bash

sudo chown -R shmir: /tmp/mfold_files
sudo chown -R shmir: /opt/shmir/databases

exec $@
