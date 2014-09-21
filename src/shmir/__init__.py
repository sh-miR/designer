"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys
import os

from flask import Flask
from flask.ext.cache import Cache

from data.models import Backbone


__all__ = ['app', 'run']

cache = Cache(config={
    'CACHE_TYPE': 'redis', 'CACHE_DEFAULT_TIMEOUT': 3600
})
app = Flask(__name__)
app.config.from_object('shmir.settings')
cache.init_app(app)

# Fixing celery path
sys.path.append(os.getcwd())

# Import which is needed to register views
# pylint: disable=W0611
import shmir.views

Backbone.generate_regexp_all()
