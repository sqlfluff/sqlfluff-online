import os

from gevent.pywsgi import WSGIServer

from . import create_app

app = create_app()
port = int(os.getenv("PORT", "5000"))

http_server = WSGIServer(("0.0.0.0", port), app)

if __name__ == "__main__":
    http_server.serve_forever()
