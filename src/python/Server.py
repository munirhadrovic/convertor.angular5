import SimpleHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import time
from grab_pics import download_all_images, get_all_images
import json

HOST_NAME = 'localhost'
PORT_NUMBER = 8081

class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, errcode):
        # ' Set headers of request.
        self.send_response(errcode)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        # ' Respond to a GET request.
        self._set_headers(200)
        parsed_path = urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
            print params
        except Exception as e:
            print e
        if parsed_path[2][1:] == 'get_pics':
            try:
                urls = get_all_images(params['url'])
                self.send_response(200,urls)
            except Exception as e:
                print e
        if parsed_path[2][1:] == 'download_pics':
            try:
                json_res = download_all_images(params['url'])
                self.send_response(200,json.dumps(json_res))
            except Exception as e:
                print e

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'KeyboardInterrupt'
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)