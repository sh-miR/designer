"""
Flask server which provide RESTful api for mfold and shmiR designer
"""

import sys

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from flask import Flask


__all__ = ['app', 'run']


app = Flask(__name__)


# Import which is needed to register views
# pylint: disable=W0611
import shmir.views

#app.add_url_rule('/mfold', 'mfold', views.get_mfold)


def run_twisted(port):
    log.startLogging(sys.stdout)

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(port, site, interface="0.0.0.0")
    reactor.run()


def run():
    run_twisted(8080)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
