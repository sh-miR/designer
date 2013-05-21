#!/usr/bin/env python3.3

from flup.server.fcgi_fork import WSGIServer
from backbone import backbone

def backbone_wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return backbone

WSGIServer(backbone_wsgi_app, bindAddress='./fastcgi0.sock').run()
