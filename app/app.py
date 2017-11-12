
import argparse
import json
import logging
# from http://flask.pocoo.org/ tutorial
from flask import Flask, render_template, request


log = logging.getLogger("data_quality_app")

parser = argparse.ArgumentParser(description='Data quality web app')
parser.add_argument('--debug', '-d', dest='debug',
                    action='store_true',
                    help='Debug mode')

app = Flask(__name__)


@app.before_first_request
def initialize():
    logger = logging.getLogger("data_quality_app")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        """%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s"""
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/config', methods=['GET'])
def config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return json.dumps(config)


if __name__ == "__main__":
    args = parser.parse_args()

    app.run()
