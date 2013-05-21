#!/usr/bin/env python3.3

from flup.server.fcgi_fork import WSGIServer
import json
from backbone import backbone

def backbone_wsgi_app(environ, start_response):
    request_json = json.loads(environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])))
    start_response('200 OK', [('Content-Type', 'application/json')])
    return backbone(request_json)

WSGIServer(backbone_wsgi_app, bindAddress='./fastcgi0.sock').run()
