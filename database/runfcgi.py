#!/usr/bin/env python3.2

DEBUG = True

from handlers import backbone_handler
import json

def backbone_wsgi_app(environ, start_response):
    try:
        request_json = json.loads(environ['wsgi.input'].read().decode())
        start_response('200 OK', [('Content-Type', 'application/json')])
        return backbone_handler(**request_json)
    except ValueError:
        start_response('200 OK', [('Content-Type', 'application/json')])
        return "Welcome, use our application to communicate with database."

if DEBUG:
    from cherrypy import wsgiserver
    address = ('127.0.0.1', 9001)
    print("Running on %s:%s" % address)
    wsgiserver.CherryPyWSGIServer(address, backbone_wsgi_app).start()
else:
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(backbone_wsgi_app, bindAddress='./fastcgi0.sock').run()
