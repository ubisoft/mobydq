#!/usr/bin/env python
"""Main module of the data quality framework web app."""
from flask import Flask, render_template
from utils import get_parameter
import json
import logging
import sys

log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/config', methods=['GET'])
def config():
    api_config = get_parameter('api')
    return json.dumps(api_config)


if __name__ == "__main__":
    config = get_parameter('app')
    app.run(host=config['host'], port=int(config['port']), threaded=True)
