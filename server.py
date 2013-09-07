import os
import argparse

from jinja2 import Environment, FileSystemLoader

import BaseHTTPServer, SimpleHTTPServer


class Server(BaseHTTPServer.HTTPServer):

    def __init__(self, *args, **kwargs):
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)
        self.jinja_env = Environment(loader=FileSystemLoader('.'))


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def render_template(self):
        template = self.server.jinja_env.get_template(self.path)
        return template.render(the='variables', go='here')

    def serve_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.path = self.path.strip('/')

        if not self.path:
            self.path = 'index.html'

        self.wfile.write(self.render_template())

    def do_GET(self):

        file_ext = os.path.splitext(self.path)[1]

        if self.path == '/' or file_ext == '.html' or file_ext == '.htm':
            return self.serve_html()

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def run_from_cli():
    parser = argparse.ArgumentParser(description="Server")

    parser.add_argument('--base_path', dest='base_path', default=None,
                        help="Base directory to serve files from.")


    args = vars(parser.parse_args())

    if args['base_path']:
        os.chdir(args['base_path'])

    httpd = Server(('', 8005), RequestHandler)

    try:
        print 'Mobile Server started at port 8005 ...'
        httpd.serve_forever()
    except:
        print 'Server shutting down'
        httpd.socket.close()


if __name__ == '__main__':
    run_from_cli()