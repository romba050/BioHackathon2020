"""
This file is part of the OpenProtein project.

For license information, please see the LICENSE file in the root directory.

Serves the live dashboard while training runs. The training loop pushes its
latest evaluation results with `set_graph_data`, and the dashboard frontend
(built from the `dashboard/` folder) polls them back from `/graph`. Both the
frontend and the data are served from the same port, so the frontend needs no
configuration to find the backend.
"""

import logging
import os
import socket
import threading

import flask.cli
from flask import Flask, jsonify, request, send_from_directory

DEFAULT_PORT = 5050
DASHBOARD_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "dashboard", "build")
BUILD_INSTRUCTIONS = "make dashboard   (or: npm --prefix dashboard install " \
                     "&& npm --prefix dashboard run build)"

APP = Flask(__name__, static_folder=DASHBOARD_BUILD_DIR, static_url_path="")
DATA = None
DATA_LOCK = threading.Lock()


def set_graph_data(data):
    """Called by the training loop with the latest evaluation results."""
    global DATA
    with DATA_LOCK:
        DATA = data


@APP.route("/graph", methods=["GET"])
def get_graph():
    with DATA_LOCK:
        return jsonify(DATA)


@APP.route("/graph", methods=["POST"])
def update_graph():
    """Kept so an external process can also push results to the dashboard."""
    set_graph_data(request.json)
    return jsonify({"result": "OK"})


@APP.route("/")
def index():
    if not dashboard_is_built():
        return ("<h1>OpenProtein dashboard not built</h1>"
                "<p>The training data is being served at <a href='/graph'>/graph</a>, "
                "but the frontend has not been built yet. Run:</p>"
                f"<pre>{BUILD_INSTRUCTIONS}</pre>"
                "<p>then reload this page.</p>", 503)
    return send_from_directory(DASHBOARD_BUILD_DIR, "index.html")


def dashboard_is_built():
    return os.path.isfile(os.path.join(DASHBOARD_BUILD_DIR, "index.html"))


def pick_port(preferred):
    """Return `preferred` if it is free, otherwise a free port chosen by the OS."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", preferred))
            return preferred
        except OSError:
            pass
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]


class GraphWebServer(threading.Thread):
    def __init__(self, port):
        # Daemon thread so the process can exit cleanly. Python 3.12 cannot spawn
        # request handler threads once the interpreter starts shutting down, so a
        # non-daemon server would linger but fail every request.
        threading.Thread.__init__(self, daemon=True)
        self.port = port

    def run(self):
        logging.basicConfig(filename="output/app.log", level=logging.DEBUG)
        # The CLI banner would interleave with the training log; the URL is
        # printed by op_cli instead.
        flask.cli.show_server_banner = lambda *args, **kwargs: None
        APP.run(debug=False, host="0.0.0.0", port=self.port)


def start_dashboard_server(preferred_port=DEFAULT_PORT):
    """Start serving the dashboard in the background and return its URL."""
    port = pick_port(preferred_port)
    GraphWebServer(port).start()
    return f"http://localhost:{port}/"
