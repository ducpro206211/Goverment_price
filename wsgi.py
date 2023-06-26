from gevent.pywsgi import WSGIServer
from main import app

import os

PORT = int(os.getenv('PORT', '9000'))

if __name__ == '__main__':
    print("done")
    http_server = WSGIServer(('0.0.0.0', PORT), app)
    http_server.serve_forever()