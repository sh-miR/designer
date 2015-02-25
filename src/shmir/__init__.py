"""
.. module:: shmir
    :synopsis: Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys
import os

from flask import Flask
from flask.ext.cache import Cache
from sqlalchemy import exc as sqlalchemy_exc

from data.models import Backbone


__all__ = ['app', 'run']

app = Flask(__name__)
app.config.from_object(
    os.environ.get('SHMIR_SETTINGS_MODULE', 'shmir.settings'))
cache = Cache(app)

# Fixing celery path
sys.path.append(os.getcwd())

import shmir.views  # noqa

# Generating all regexps, if database exists
try:
    Backbone.generate_regexp_all()
except (sqlalchemy_exc.OperationalError, sqlalchemy_exc.ProgrammingError):
    pass
