"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys
import os

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
app.config.from_object('shmir.settings')
cache.init_app(app)

# Fixing celery path
sys.path.append(os.getcwd())

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
