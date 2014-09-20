"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys
import os

from kombu import Queue

from flask import Flask

from data.models import Backbone


__all__ = ['app', 'run']


app = Flask(__name__)

# Fixing celery path
sys.path.append(os.getcwd())

# TODO move config to proper place
app.config['CELERYD_FORCE_EXECV'] = True
app.config['CELERY_QUEUES'] = (
    Queue('celery', routing_key='celery'),
    Queue('subtasks', routing_key='transient',
          delivery_mode=1),
)
app.config['DEBUG'] = True

# Import which is needed to register views
# pylint: disable=W0611
import shmir.views

Backbone.generate_regexp_all()
