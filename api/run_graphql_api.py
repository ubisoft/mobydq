from database.base import dbSession
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema
import api_utils
import logging
import sys

log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)
app.add_url_rule('/dataquality/api/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbSession.remove()


if __name__ == '__main__':
    api_utils.init()
    config = api_utils.get_parameter('api')
    app.run(host=config['host'], port=int(config['port']), threaded=True, debug=True)
