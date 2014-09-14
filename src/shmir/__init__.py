"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys
import os

from kombu import Queue

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from flask import Flask
from flask.ext.cache import Cache

from data.models import Backbone


__all__ = ['app', 'run']

cache = Cache(config={
    'CACHE_TYPE': 'redis', 'CACHE_DEFAULT_TIMEOUT': 3600
})
app = Flask(__name__)
cache.init_app(app)

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


def run_twisted(port):
    Backbone.generate_regexp_all()

    log.startLogging(sys.stdout)

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(port, site, interface="0.0.0.0")
    reactor.run()


def run():
    run_twisted(8080)
