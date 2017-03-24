#!/usr/bin/env python3

"""Docstring..."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
from data_access import APIObj
import json


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        self.api_obj = APIObj()
        path_list = urlsplit(self.path).path.split("/")
        try:
            if path_list[1] == "api":
                if path_list[2] == "datasets":
                    response = self.api_obj.datasets
                elif path_list[2] == "meta":
                    response = self.api_obj.meta[path_list[3]]
                response = json.dumps(response)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(response, 'utf8'))
                return
        except:
            self.send_404()

    def do_POST(self):
        self.api_obj = APIObj()
        path_list = urlsplit(self.path).path.split("/")
        if path_list[1] == "api":
            self.send_response(200)
            self.end_headers()
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            response = "YOU ASKED FOR: " + post_body.decode('utf8')
            self.wfile.write(bytes(response, 'utf8'))
            return
        self.send_404()

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        response = "The page you're looking for doesn't exist."
        self.wfile.write(bytes(response, 'utf8'))
            

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
