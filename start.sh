#!/bin/bash

# If we mount host's directory as Docker volume, it will not contain
# any egg-related files. Therefore we should ensure that shmir is installed
# in "develop" mode every time.
pip install -e /opt/shmir

exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
