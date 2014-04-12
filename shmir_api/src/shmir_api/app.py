"""
Flask server which provide RESTful api for database and mfold
"""

import sys

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from flask import Flask

from shmir_api.database.database import disconnect
from shmir_api.database import handlers as db_handlers
from shmir_api.mfold import handlers as mfold_handlers


app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    disconnect()


app.add_url_rule('/mfold', 'mfold', mfold_handlers.get_mfold)


def run():
    log.startLogging(sys.stdout)

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(8080, site, interface="0.0.0.0")
    reactor.run()
