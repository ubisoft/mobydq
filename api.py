"""Main module of the data quality framework API."""
from flask import Blueprint, Flask, request
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
import api_utils
import socket

app = Flask(__name__)
CORS(app)

# Create blue print to indicate api base url
blueprint = Blueprint('api', __name__, url_prefix='/dataquality/api')
api = Api(
    blueprint,
    title='Data Quality Framework API',
    version='v1',
    description='RESTful API to perform CRUD operations on the Data Quality Framework database.',
    doc='/doc')
app.register_blueprint(blueprint)


# BatchOwner
nsBatchOwner = api.namespace('BatchOwner', path='/v1')
mdBatchOwner = api.model(
    'BatchOwner',
    {'id': fields.Integer(required=False, description='Batch owner Id'),
        'name': fields.String(required=False, description='Batch owner name')})


@nsBatchOwner.route('/batchowners')
class BatchOwner(Resource):
    """Class for Batch Owner API endpoints."""

    @nsBatchOwner.expect(api.models['BatchOwner'], validate=True)
    def post(self):
        """
        Create Batch Owner.

        Use this method to create a Batch Owner.
        """
        return api_utils.create('BatchOwner', request.json)

    def get(self):
        """
        Get list of Batch Owners.

        Use this method to get the list of Batch Owners.
        """
        return api_utils.read('BatchOwner')

    @nsBatchOwner.expect(api.models['BatchOwner'], validate=True)
    def put(self):
        """
        Update Batch Owner.

        Use this method to update a Batch Owner.
        """
        return api_utils.update('BatchOwner', request.json)

    @nsBatchOwner.expect(api.models['BatchOwner'], validate=True)
    def delete(self):
        """
        Delete Batch Owner.

        Use this method to delete a Batch Owner.
        """
        return api_utils.read('BatchOwner', request.json)


# DataSource
nsDataSource = api.namespace('DataSource', path='/v1')
mdDataSource = api.model(
    'DataSource',
    {'id': fields.Integer(required=False, description='Data source Id'),
        'name': fields.String(required=False, description='Data source name'),
        'dataSourceTypeId': fields.Integer(required=False, description='Data source type Id'),
        'connectionString': fields.String(required=False, description='ODBC Connection sring'),
        'login': fields.String(required=False, description='Login'),
        'password': fields.String(required=False, description='Password')})


@nsDataSource.route('/datasources')
class DataSource(Resource):
    """Class for Data Source API endpoints."""

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def post(self):
        """
        Create Data Source.

        Use this method to create a Data Source.
        """
        return api_utils.create('DataSource', request.json)

    def get(self):
        """
        Get list of Data Sources.

        Use this method to get the list of Data Sources.
        """
        return api_utils.read('DataSource')

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def put(self):
        """
        Update Data Source.

        Use this method to update a Data Source.
        """
        return api_utils.update('DataSource', request.json)

    @nsDataSource.expect(api.models['DataSource'], validate=True)
    def delete(self):
        """
        Delete Data Source.

        Use this method to delete a Data Source.
        """
        return api_utils.delete('DataSource', request.json)


# DataSourceType
nsDataSourceType = api.namespace('DataSourceType', path='/v1')
mdDataSourceType = api.model(
    'DataSourceType',
    {'id': fields.Integer(required=False, description='Data source type Id'),
        'name': fields.String(required=False, description='Data source type name')})


@nsDataSourceType.route('/datasourcetypes')
class DataSourceType(Resource):
    """Class for Data Source Type API endpoints."""

    @nsDataSourceType.expect(api.models['DataSourceType'], validate=True)
    def post(self):
        """
        Create Data Source Type.

        Use this method to create a Data Source Type.
        """
        return api_utils.create('DataSourceType', request.json)

    def get(self):
        """
        Get list of Data Source Types.

        Use this method to get the list of Data Source Types.
        """
        return api_utils.read('DataSourceType')

    @nsDataSourceType.expect(api.models['DataSourceType'], validate=True)
    def put(self):
        """
        Update Data Source Type.

        Use this method to update a Data Source Type.
        """
        return api_utils.update('DataSourceType', request.json)

    @nsDataSourceType.expect(api.models['DataSourceType'], validate=True)
    def delete(self):
        """
        Delete Data Source Type.

        Use this method to delete a Data Source Type.
        """
        return api_utils.delete('DataSourceType', request.json)

# EventType
nsEventType = api.namespace('EventType', path='/v1')
mdEventType = api.model(
    'EventType',
    {'id': fields.Integer(required=False, description='Event type type Id'),
        'name': fields.String(required=False, description='Event type name')})


@nsEventType.route('/eventtypes')
class EventType(Resource):
    """Class for Event Type API endpoints."""

    @nsEventType.expect(api.models['EventType'], validate=True)
    def post(self):
        """
        Create Event Type.

        Use this method to create an Event Type.
        """
        return api_utils.create('EventType', request.json)

    def get(self):
        """
        Get list of Event Types.

        Use this method to get the list of Event Types.
        """
        return api_utils.read('EventType')

    @nsEventType.expect(api.models['EventType'], validate=True)
    def put(self):
        """
        Update Event Type.

        Use this method to update an Event Type.
        """
        return api_utils.update('EventType', request.json)

    @nsEventType.expect(api.models['EventType'], validate=True)
    def delete(self):
        """
        Delete Event Type.

        Use this method to delete an Event Type.
        """
        return api_utils.delete('EventType', request.json)


# Indicator
nsIndicator = api.namespace('Indicator', path='/v1')
mdIndicator = api.model(
    'Indicator',
    {'id': fields.Integer(required=False, description='Indicator Id'),
        'name': fields.String(required=False, description='Indicator name'),
        'description': fields.String(required=False, description='Indicator description'),
        'indicatorTypeId': fields.Integer(required=False, description='Indicator type Id'),
        'batchOwnerId': fields.Integer(required=False, description='Batch owner Id'),
        'executionOrder': fields.Integer(required=False, description='Execution order'),
        'alertOperator': fields.String(required=False, description='Alert operator'),
        'alertThreshold': fields.String(required=False, description='Alert threshold'),
        'distributionList': fields.String(required=False, description='Comma separated list of e-mails'),
        'active': fields.Integer(required=False, description='Active flag: 1 or 0')})


@nsIndicator.route('/indicators')
class Indicator(Resource):
    """Class for Indicator API endpoints."""

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def post(self):
        """
        Create Indicator.

        Use this method to create an Indicator.
        """
        return api_utils.create('Indicator', request.json)

    def get(self):
        """
        Get list of Indicator.

        Use this method to get the list of Indicators.
        """
        return api_utils.read('Indicator')

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def put(self):
        """
        Update Indicator.

        Use this method to update an Indicator.
        """
        return api_utils.update('Indicator', request.json)

    @nsIndicator.expect(api.models['Indicator'], validate=True)
    def delete(self):
        """
        Delete Indicator.

        Use this method to delete an Indicator.
        """
        return api_utils.delete('Indicator', request.json)


# IndicatorParameter
mdIndicatorParameter = api.model(
    'IndicatorParameter',
    {'id': fields.Integer(required=False, description='Indicator parameter Id'),
        'name': fields.String(required=False, description='Indicator parameter name'),
        'value': fields.String(required=False, description='Indicator parameter value')})


@nsIndicator.route('/indicators/<int:indicatorid>/indicatorparameters')
@nsIndicator.param('indicatorid', 'Indicator Id')
class IndicatorParameter(Resource):
    """Class for Indicator Parameter API endpoints."""

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def post(self, indicatorid):
        """
        Create Indicator Parameter.

        Use this method to create an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicatorid
        return api_utils.create('IndicatorParameter', parameters)

    def get(self, indicatorid):
        """
        Get list of Indicator Parameter.

        Use this method to get the list of Indicator Parameters.
        """
        parameters = {}
        parameters['indicatorId'] = indicatorid
        return api_utils.read('IndicatorParameter', parameters)

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def put(self, indicatorid):
        """
        Update Indicator Parameter.

        Use this method to update an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicatorid
        return api_utils.update('IndicatorParameter', parameters)

    @nsIndicator.expect(api.models['IndicatorParameter'], validate=True)
    def delete(self, indicatorid):
        """
        Delete Indicator Parameter.

        Use this method to delete an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicatorid
        return api_utils.delete('IndicatorParameter', parameters)


# IndicatorType
nsIndicatorType = api.namespace('IndicatorType', path='/v1')
mdIndicatorType = api.model(
    'IndicatorType',
    {'id': fields.Integer(required=False, description='Indicator type Id'),
        'name': fields.String(required=False, description='Indicator type name'),
        'module': fields.String(required=False, description='Indicator type module name'),
        'function': fields.String(required=False, description='Indicator type function name')})


@nsIndicatorType.route('/indicatortypes')
class IndicatorType(Resource):
    """Class for Indicator Type API endpoints."""

    @nsIndicatorType.expect(api.models['IndicatorType'], validate=True)
    def post(self):
        """
        Create Indicator Type.

        Use this method to create an Indicator Type.
        """
        return api_utils.create('IndicatorType')

    def get(self):
        """
        Get list of Indicator Types.

        Use this method to get the list of Indicator Types.
        """
        return api_utils.read('IndicatorType')

    @nsIndicatorType.expect(api.models['IndicatorType'], validate=True)
    def put(self):
        """
        Update Indicator Type.

        Use this method to update an Indicator Type.
        """
        return api_utils.update('IndicatorType')

    @nsIndicatorType.expect(api.models['IndicatorType'], validate=True)
    def delete(self):
        """
        Delete Indicator Type.

        Use this method to delete an Indicator Type.
        """
        return api_utils.delete('IndicatorType')


# Status
nsStatus = api.namespace('Status', path='/v1')
mdStatus = api.model(
    'Status',
    {'id': fields.Integer(required=False, description='Status Id'),
        'name': fields.String(required=False, description='Status name')})


@nsStatus.route('/status')
class Status(Resource):
    """Class for Status API endpoints."""

    @nsStatus.expect(api.models['Status'], validate=True)
    def post(self):
        """
        Create Status.

        Use this method to create a Status.
        """
        return api_utils.create('Status')

    def get(self):
        """
        Get list of Status.

        Use this method to get the list of Status.
        """
        return api_utils.read('Status')

    @nsStatus.expect(api.models['Status'], validate=True)
    def put(self):
        """
        Update Status.

        Use this method to update a Status.
        """
        return api_utils.update('Status')

    @nsStatus.expect(api.models['Status'], validate=True)
    def delete(self):
        """
        Delete Status.

        Use this method to delete a Status.
        """
        return api_utils.delete('Status')


if __name__ == '__main__':
    hostname = socket.gethostname()
    app.run(host=hostname, threaded=True, debug=True)
