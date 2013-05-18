from http.server import HTTPServer, CGIHTTPRequestHandler

HTTPServer(("", 9001), CGIHTTPRequestHandler).serve_forever()
