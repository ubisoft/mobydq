#!/usr/bin/env python
"""Main module of the data quality framework web app."""
from flask import Flask, render_template
from api.database.operation import Operation
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/config', methods=['GET'])
def config():
    config = Operation.get_parameter('api')
    return json.dumps(config)


if __name__ == "__main__":
    config = Operation.get_parameter('app')
    app.run(host=config['host'], port=config['port'], threaded=True)
