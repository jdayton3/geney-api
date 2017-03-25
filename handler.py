#!/usr/bin/env python3

"""Docstring..."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs
from data_access import APIObj
from socketserver import ThreadingMixIn
import json

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        try:
            self.api_obj = APIObj()
            path_list = urlsplit(self.path).path.split("/")
            if path_list[1] == "api":
                if path_list[2] == "datasets":
                    response = self.api_obj.datasets
                elif path_list[2] == "meta":
                    try:
                        id = path_list[3]
                        search = parse_qs(urlsplit(self.path).query)['search'][0]
                        if path_list[4] == "gene":
                            response = self.api_obj.searchGenes(search.upper())
                        else:
                            # They're looking for a meta type.
                            # TODO fix this
                            response = self.api_obj.searchGenes(search.upper())
                    except:
                        response = self.api_obj.meta[path_list[3]]
                response = json.dumps(response)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(response, 'utf8'))
        except:
            self.send_file("file.csv")
            return
            self.send_404()

    def do_POST(self):
        try:
            self.api_obj = APIObj()
            path_list = urlsplit(self.path).path.split("/")
            if path_list[1] == "api":
                self.send_response(200)
                self.end_headers()
                content_len = int(self.headers.get('content-length', 0))
                post_body = self.rfile.read(content_len)
                response = "YOU ASKED FOR: " + post_body.decode('utf8')
                self.wfile.write(bytes(response, 'utf8'))
        except:
            self.send_404()

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        response = "The page you're looking for doesn't exist."
        self.wfile.write(bytes(response, 'utf8'))
            
    def send_file(self, path):
        self.send_response(200)
        self.send_header('Content-type','text/csv') #text/tab-separated-values
        self.send_header('Content-disposition','attachment; filename=file.csv')
        self.end_headers()
        f = open(path, 'rb')
        while True:
            file_data = f.read(16777216) # Read a max of 16 MiB
            if file_data is None or len(file_data) == 0:
                break
            self.wfile.write(file_data)
#            print("Data written...")
        f.close()

def run():
    print('starting server...')

    # Server settings
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
