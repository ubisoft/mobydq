from flask import abort, Blueprint, Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_restplus import Api, fields, Resource

# Create flask app and enabe cross origin resource sharing
app = Flask(__name__)
CORS(app)


# This is required to fix swagger UI not loading issue due to https
@property
def swagger_url(self):
    """Patch for HTTPS"""
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')


# Create blueprint to indicate api base url
blueprint = Blueprint('api', __name__, url_prefix='/dq/api')

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
execute = api.namespace('Execute', path='/v1')
health = api.namespace('Health', path='/v1')

# Document parameters
parser = api.parser()
parser.add_argument('indicator_group_id', type=int, default=0, required=True, location='form', help='Id of the indicator group to be executed.')
parser.add_argument('indicator_ids', type=int, default=[0], required=False, location='form', action='append', help='List of indicator Ids from the group to be executed. All active indicators from the group are executed if this parameter is not supllied.')

# Document default responses
responses = {
    200: 'Success: The request has succeeded.',
    400: 'Bad Request: The request could not be understood by the server or is not compliant with validation rules.',
    403: 'Forbidden: You do not have sufficient permissions to access this resource.',
    404: 'Not Found: The server has not found anything matching the Requested URI.',
    500: 'Internal Server Error: The server encountered an error.'
    }

# Document response model for execute endpoint
execute_response = execute.model('Execute response', {'batch_id': fields.Integer})

@execute.route('/execute', endpoint='with-parser')
@execute.doc(responses=responses)
class Execute(Resource):
    # @execute.response(200, 'Success: The request has succeeded.', response_model)
    @execute.expect(parser, validate=True)  # Header parameters can be defined here
    @execute.response(200, 'Success: The request has succeeded.', execute_response)
    def post(self):
        """
        Execute indicators
        Use this endpoint to trigger the execution of an indicator or a group of indicators.
        """
        args = parser.parse_args(strict=True)
        # Permissions verifications
        # if not something:
            # message = {'message': 'Forbidden: You do not have sufficient permissions to access this resource.'}
            # abort(403, message)

        # Call execute method
        status, message = execute.execute_batch()

        if status:
            return jsonify(message)
        else:
            abort(500, message)


@health.route('/health')
@health.doc(responses=responses)
class Health(Resource):
    def get(self):
        """
        Get API health status
        Use this endpoint to get the health status of this API.
        """
        # Permissions verifications
        # if not something:
            # message = {'message': 'Forbidden: You do not have sufficient permissions to access this resource.'}
            # abort(403, message)

        status = True
        message = {'message': 'Success: The request has succeeded.'}

        if status:
            return jsonify(message)
        else:
            abort(500, message)


@app.after_request
def log_request(response):
    if request.method != 'OPTIONS':
        # Do something here to log http requests
        pass
        return response
