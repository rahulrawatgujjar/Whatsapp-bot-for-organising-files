#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
path=sys.argv[1]
print(sys.argv)


def run_localhost_8081(path):
    os.chdir(path)
    PORT = 8081
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving file at http://localhost:%s" % PORT)
        httpd.serve_forever()

run_localhost_8081(path)