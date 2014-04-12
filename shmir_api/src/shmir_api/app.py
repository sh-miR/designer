"""
Flask server which provide RESTful api for database and mfold
"""

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import Flask

from shmir_api.database.database import disconnect
from shmir_api.database import handlers as db_handlers
from shmir_api.mfold import handlers as mfold_handlers


app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    disconnect()


#backwards compatibility
app.add_url_rule('/database/get_all', 'database.get_all',
                 db_handlers.backbone_get_all)
app.add_url_rule('/database/get_by_name', 'database.get_by_name',
                 db_handlers.backbone_get_by_name)
app.add_url_rule('/database/get_by_mirna_s', 'database.get_by_miRNA_s',
                 db_handlers.backbone_get_by_miRNA_s)


app.add_url_rule('/database/backbone/get_all',
                 'database.backbone.get_all',
                 db_handlers.backbone_get_all)
app.add_url_rule('/database/backbone/get_by_name',
                 'database.backbone.get_by_name',
                 db_handlers.backbone_get_by_name)
app.add_url_rule('/database/backbone/get_by_mirna_s',
                 'database.backbone.get_by_miRNA_s',
                 db_handlers.backbone_get_by_miRNA_s)
app.add_url_rule('/database/immuno/get_all',
                 'database.immuno.get_all',
                 db_handlers.immuno_get_all)
app.add_url_rule('/mfold', 'mfold', mfold_handlers.get_mfold)


def run():
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(8080, site, interface="0.0.0.0")
    reactor.run()
