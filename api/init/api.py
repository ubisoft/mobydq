from batch import Batch
from data_source import DataSource
from flask import abort, Blueprint, Flask, jsonify, request, url_for
from flask_restplus import Api, Resource
import logging
import sys
import utils


log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create flask app and enabe cross origin resource sharing
app = Flask(__name__)


# This is required to fix swagger UI not loading issue due to https
@property
def swagger_url(self):
    """Patch for HTTPS"""
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')


# Create blueprint to indicate api base url
blueprint = Blueprint('api', __name__, url_prefix='/data-quality/api')

# Create Swagger documentation for blueprint
api = Api(
    blueprint,
    title='Data Quality Framework API',
    version='v1',
    description='''API used to trigger the execution of data quality indicators.''',
    doc='/doc',
    contact='to be configured')
# Api.specs_url = swagger_url  # To be activated after we implement https
app.register_blueprint(blueprint)

# Declare resources name spaces
api.namespaces.clear()
graphql = api.namespace('GraphQL', path='/v1')
health = api.namespace('Health', path='/v1')

# Document headers and other parameters
parser = api.parser()
parser.add_argument('query', type=str, required=True, location='form', help='GraphQL query or mutation.')

# Document default responses
responses = {
    200: 'Success: The request has succeeded.',
    400: 'Bad Request: The request could not be understood by the server or is not compliant with validation rules.',
    403: 'Forbidden: You do not have sufficient permissions to access this resource.',
    404: 'Not Found: The server has not found anything matching the Requested URI.',
    500: 'Internal Server Error: The server encountered an error.'
    }


@graphql.route('/graphql', endpoint='with-parser')
@graphql.doc(responses=responses)
class GraphQL(Resource):
    @graphql.expect(parser, validate=True)  # Header parameters can be defined here
    def post(self):
        """
        Execute queries and mutations
        Use this endpoint to send http request to the GraphQL API.
        """
        args = parser.parse_args(strict=True)

        # Execute request on GraphQL API
        status, data = utils.execute_graphql_request(args['query'])

        # Execute batch of indicators
        if status == 200 and 'executeBatch' in args['query']:
            batch_id = str(data['data']['executeBatch']['batch']['id'])
            batch = Batch()
            batch.execute(batch_id)

        # Test connectivity to a data source
        if status == 200 and 'testDataSource' in args['query']:
            data_source_id = str(data['data']['testDataSource']['dataSource']['id'])
            data_source = DataSource()
            data = data_source.test(data_source_id)

        if status == 200:
            return jsonify(data)
        else:
            abort(500, data)


@health.route('/health')
@health.doc(responses=responses)
class Health(Resource):
    def get(self):
        """
        Get API health status
        Use this endpoint to get the health status of this API.
        """
        status = 200
        message = {'message': 'Success: The request has succeeded.'}

        if status == 200:
            return jsonify(message)
        else:
            abort(500, message)


@app.after_request
def log_request(response):
    if request.method != 'OPTIONS':
        # Do something here to log http requests
        pass
        return response
