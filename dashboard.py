"""
This file is part of the OpenProtein project.

For license information, please see the LICENSE file in the root directory.
"""

import logging
import os
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# Port 5000 is taken by the AirPlay Receiver on recent macOS versions, in which
# case set OPENPROTEIN_DASHBOARD_PORT to a free port.
DASHBOARD_PORT = int(os.environ.get("OPENPROTEIN_DASHBOARD_PORT", "5000"))
DASHBOARD_URL = f"http://localhost:{DASHBOARD_PORT}/graph"

APP = Flask(__name__)
CORS = CORS(APP)
DATA = None


@APP.route('/graph', methods=['POST'])
def update_graph():
    global DATA
    DATA = request.json
    return jsonify({"result": "OK"})


@APP.route('/graph', methods=['GET'])
@cross_origin()
def get_graph():
    return jsonify(DATA)

class GraphWebServer(threading.Thread):
    def __init__(self):
        # Daemon thread so the process exits when training completes. Python 3.12
        # cannot spawn request handler threads once the interpreter starts shutting
        # down, so a non-daemon server would linger but fail every request.
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        logging.basicConfig(filename="output/app.log", level=logging.DEBUG)
        APP.run(debug=False, host='0.0.0.0', port=DASHBOARD_PORT)

def start_dashboard_server():
    flask_thread = GraphWebServer()
    flask_thread.start()
