"""Run the wsgi server."""
import argparse
import os

from gevent.pywsgi import WSGIServer

from . import create_app

app = create_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=None)
    args = parser.parse_args()

    port = args.port or int(os.getenv("PORT", "5000"))

    http_server = WSGIServer(("0.0.0.0", port), app)
    http_server.serve_forever()
