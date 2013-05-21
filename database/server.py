from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 9001

print("Running server http://127.0.0.1:%d" % PORT)

handler = CGIHTTPRequestHandler
handler.cgi_directories = ['']
HTTPServer(("", PORT), handler).serve_forever()
