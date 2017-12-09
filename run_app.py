#!/usr/bin/env python
"""Main module of the data quality framework web app."""
from flask import Flask, render_template
from api.database.operation import Operation
import json
import socket

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/config', methods=['GET'])
def config():
    config = Operation.get_parameter('app')
    return json.dumps(config)


if __name__ == "__main__":
    host_name = socket.gethostname()
    app.run(host=host_name, port=5001, threaded=True)
