"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys

from kombu import Queue

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from flask import Flask

from data.models import Backbone


__all__ = ['app', 'run']


app = Flask(__name__)


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
