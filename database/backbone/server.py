from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 9001

print("Running server http://127.0.0.1:%d" % PORT)

HTTPServer(("", PORT), CGIHTTPRequestHandler).serve_forever()
