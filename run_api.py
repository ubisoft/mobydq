#!/usr/bin/env python
"""Main module of the data quality framework API."""
from flask import Blueprint, Flask, request
from flask_cors import CORS
from flask_restplus import Api, fields, Resource
from api.batch_method import BatchMethod
from api.database.operation import Operation
import api.utils as utils

app = Flask(__name__)
CORS(app)
config = Operation.get_parameter('api')

# Create blue print to indicate api_object base url
blueprint = Blueprint('api_object', __name__, url_prefix='/dataquality/api')
api_object = Api(
    blueprint,
    title='Data Quality Framework API',
    version='v1',
    description='RESTful API for the Data Quality Framework. Base URL: http://{}:5000/dataquality/api'.format(config['host']),
    doc='/doc')
app.register_blueprint(blueprint)

# List of namespaces used by the endpoints below
nsBatch = api_object.namespace('Batch', path='/v1')
nsDataSource = api_object.namespace('DataSource', path='/v1')
nsEvent = api_object.namespace('Event', path='/v1')
nsIndicator = api_object.namespace('Indicator', path='/v1')
nsSession = api_object.namespace('Session', path='/v1')
nsStatus = api_object.namespace('Status', path='/v1')


# Batch namespace
@nsBatch.route('/batchowners')
class BatchOwnerList(Resource):
    mdBatchOwner = api_object.model(
        'BatchOwner',
        {'id': fields.Integer(required=False, description='Batch owner Id'),
            'name': fields.String(required=False, description='Batch owner name')})

    @nsBatch.expect(mdBatchOwner, validate=True)
    def post(self):
        """
        Create Batch Owner.
        Use this method to create a Batch Owner.
        """
        return utils.create('BatchOwner', request.json)

    def get(self):
        """
        Get list of Batch Owners.
        Use this method to get the list of Batch Owners.
        """
        return utils.read('BatchOwner')

    @nsBatch.expect(mdBatchOwner, validate=True)
    def put(self):
        """
        Update Batch Owner.
        Use this method to update a Batch Owner.
        """
        return utils.update('BatchOwner', request.json)

    @nsBatch.expect(mdBatchOwner, validate=True)
    def delete(self):
        """
        Delete Batch Owner.
        Use this method to delete a Batch Owner.
        """
        return utils.delete('BatchOwner', request.json)


@nsBatch.route('/batchowners/<int:batch_owner_id>')
@nsBatch.param('batch_owner_id', 'Batch Owner Id')
class BatchOwner(Resource):
    def get(self, batch_owner_id):
        """
        Get Batch Owner.
        Use this method to get the details of a Batch Owner.
        """
        parameters = {'id': batch_owner_id}
        return utils.read('BatchOwner', parameters)


@nsBatch.route('/batchowners/<int:batch_owner_id>/batches')
@nsBatch.param('batch_owner_id', 'Batch Owner Id')
class BatchOwnerBatch(Resource):
    def get(self, batch_owner_id):
        """
        Get list of Batches.
        Use this method to get a Batch Owner's list of Batches.
        """
        parameters = {'batchOwnerId': batch_owner_id}
        return utils.read('Batch', parameters)


@nsBatch.route('/batchowners/<int:batch_owner_id>/execute')
@nsBatch.param('batch_owner_id', 'Batch Owner Id')
class BatchOwnerExecute(Resource):
    def post(self, batch_owner_id):
        """
        Execute a Batch.
        Use this method to execute a Batch Owner's Indicators.
        """
        return BatchMethod(batch_owner_id).execute()


# Data source namespace
@nsDataSource.route('/datasources')
class DataSourceList(Resource):
    mdDataSource = api_object.model(
        'DataSource',
        {'id': fields.Integer(required=False, description='Data source Id'),
            'name': fields.String(required=False, description='Data source name'),
            'dataSourceTypeId': fields.Integer(required=False, description='Data source type Id'),
            'connectionString': fields.String(required=False, description='ODBC Connection sring'),
            'login': fields.String(required=False, description='Login'),
            'password': fields.String(required=False, description='Password')})

    @nsDataSource.expect(api_object.models['DataSource'], validate=True)
    def post(self):
        """
        Create Data Source.
        Use this method to create a Data Source.
        """
        return utils.create('DataSource', request.json)

    def get(self):
        """
        Get list of Data Sources.
        Use this method to get the list of Data Sources.
        """
        return utils.read('DataSource')

    @nsDataSource.expect(api_object.models['DataSource'], validate=True)
    def put(self):
        """
        Update Data Source.
        Use this method to update a Data Source.
        """
        return utils.update('DataSource', request.json)

    @nsDataSource.expect(api_object.models['DataSource'], validate=True)
    def delete(self):
        """
        Delete Data Source.
        Use this method to delete a Data Source.
        """
        return utils.delete('DataSource', request.json)


@nsDataSource.route('/datasources/<int:data_source_id>')
@nsDataSource.param('data_source_id', 'Data Source Id')
class DataSource(Resource):
    def get(self, data_source_id):
        """
        Get Data Source.
        Use this method to get a Data Source.
        """
        parameters = {'id': data_source_id}
        return utils.read('DataSource', parameters)


@nsDataSource.route('/datasources/<int:data_source_id>/test')
@nsDataSource.param('data_source_id', 'Data Source Id')
class DataSourceTest(Resource):
    def post(self, data_source_id):
        """
        Test Data Source.
        Use this method to test connectivity to a Data Source.
        """
        pass
        return {'message': 'Not implemented yet'}


@nsDataSource.route('/datasourcetypes')
class DataSourceTypeList(Resource):
    mdDataSourceType = api_object.model(
        'DataSourceType',
        {'id': fields.Integer(required=False, description='Data source type Id'),
            'name': fields.String(required=False, description='Data source type name')})

    @nsDataSource.expect(api_object.models['DataSourceType'], validate=True)
    def post(self):
        """
        Create Data Source Type.
        Use this method to create a Data Source Type.
        """
        return utils.create('DataSourceType', request.json)

    def get(self):
        """
        Get list of Data Source Types.
        Use this method to get the list of Data Source Types.
        """
        return utils.read('DataSourceType')

    @nsDataSource.expect(api_object.models['DataSourceType'], validate=True)
    def put(self):
        """
        Update Data Source Type.
        Use this method to update a Data Source Type.
        """
        return utils.update('DataSourceType', request.json)

    @nsDataSource.expect(api_object.models['DataSourceType'], validate=True)
    def delete(self):
        """
        Delete Data Source Type.
        Use this method to delete a Data Source Type.
        """
        return utils.delete('DataSourceType', request.json)


# Event namespace
@nsEvent.route('/eventtypes')
class EventTypeList(Resource):
    mdEventType = api_object.model(
        'EventType',
        {'id': fields.Integer(required=False, description='Event type Id'),
            'name': fields.String(required=False, description='Event type name')})

    @nsEvent.expect(api_object.models['EventType'], validate=True)
    def post(self):
        """
        Create Event Type.
        Use this method to create an Event Type.
        """
        return utils.create('EventType', request.json)

    def get(self):
        """
        Get list of Event Types.
        Use this method to get the list of Event Types.
        """
        return utils.read('EventType')

    @nsEvent.expect(api_object.models['EventType'], validate=True)
    def put(self):
        """
        Update Event Type.
        Use this method to update an Event Type.
        """
        return utils.update('EventType', request.json)

    @nsEvent.expect(api_object.models['EventType'], validate=True)
    def delete(self):
        """
        Delete Event Type.
        Use this method to delete an Event Type.
        """
        return utils.delete('EventType', request.json)


# Indicator namespace
@nsIndicator.route('/indicators')
class IndicatorList(Resource):
    mdIndicator = api_object.model(
        'Indicator',
        {'id': fields.Integer(required=False, description='Indicator Id'),
            'name': fields.String(required=False, description='Indicator name'),
            'description': fields.String(required=False, description='Indicator description'),
            'indicatorTypeId': fields.Integer(required=False, description='Indicator type Id'),
            'batchOwnerId': fields.Integer(required=False, description='Batch owner Id'),
            'executionOrder': fields.Integer(required=False, description='Execution order'),
            'active': fields.Integer(required=False, description='Active flag: 1 or 0')})

    @nsIndicator.expect(api_object.models['Indicator'], validate=True)
    def post(self):
        """
        Create Indicator.
        Use this method to create an Indicator.
        """
        return utils.create('Indicator', request.json)

    def get(self):
        """
        Get list of Indicators.
        Use this method to get the list of Indicators.
        """
        return utils.read('Indicator')

    @nsIndicator.expect(api_object.models['Indicator'], validate=True)
    def put(self):
        """
        Update Indicator.
        Use this method to update an Indicator.
        """
        return utils.update('Indicator', request.json)

    @nsIndicator.expect(api_object.models['Indicator'], validate=True)
    def delete(self):
        """
        Delete Indicator.
        Use this method to delete an Indicator.
        """
        return utils.delete('Indicator', request.json)


@nsIndicator.route('/indicators/<int:indicator_id>')
@nsIndicator.param('indicator_id', 'Indicator Id')
class Indicator(Resource):
    def get(self, indicator_id):
        """
        Get Indicator.
        Use this method to get the details of an Indicator.
        """
        parameters = {}
        parameters['id'] = indicator_id
        return utils.read('Indicator', parameters)


@nsIndicator.route('/indicators/<int:indicator_id>/execute')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorExecute(Resource):
    def post(self, indicator_id):
        """
        Execute Indicator.
        Use this method to execute an Indicator.
        """
        parameters = {}
        parameters['id'] = indicator_id
        indicator = utils.read('Indicator', parameters)
        return BatchMethod(indicator[0]['batchOwnerId']).execute(indicator_id)


@nsIndicator.route('/indicators/<int:indicator_id>/parameters')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorParameterList(Resource):
    mdParameter = api_object.model(
        'IndicatorParameter',
        {'id': fields.Integer(required=False, description='Indicator parameter Id'),
            'name': fields.String(required=False, description='Indicator parameter name'),
            'value': fields.String(required=False, description='Indicator parameter value')})

    @nsIndicator.expect([mdParameter], validate=True)
    def post(self, indicator_id):
        """
        Create Indicator Parameter.
        Use this method to create an Indicator Parameter.
        """
        response = []
        parameters = request.json
        for parameter in parameters:
            parameter['indicatorId'] = indicator_id
            response.append(utils.create('IndicatorParameter', parameter))
        return response

    def get(self, indicator_id):
        """
        Get list of Indicator Parameters.
        Use this method to get the list of Indicator Parameters.
        """
        parameters = {}
        parameters['indicatorId'] = indicator_id
        return utils.read('IndicatorParameter', parameters)

    @nsIndicator.expect([mdParameter], validate=True)
    def put(self, indicator_id):
        """
        Update Indicator Parameter.
        Use this method to update an Indicator Parameter.
        """
        response = []
        parameters = request.json
        for parameter in parameters:
            parameter['indicatorId'] = indicator_id
            response.append(utils.update('IndicatorParameter', parameter))
        return response

    @nsIndicator.expect(mdParameter, validate=True)
    def delete(self, indicator_id):
        """
        Delete Indicator Parameter.
        Use this method to delete an Indicator Parameter.
        """
        parameters = request.json
        parameters['indicatorId'] = indicator_id
        return utils.delete('IndicatorParameter', parameters)


@nsIndicator.route('/indicators/<int:indicator_id>/results')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorResult(Resource):
    def get(self, indicator_id):
        """
        Get list of Indicator Results.
        Use this method to get the list of Indicator Results.
        """
        parameters = {}
        parameters['indicatorId'] = indicator_id
        return utils.read('IndicatorResult', parameters)


@nsIndicator.route('/indicators/<int:indicator_id>/sessions')
@nsIndicator.param('indicator_id', 'Indicator Id')
class IndicatorSession(Resource):
    def get(self, indicator_id):
        """
        Get list of Indicator Sessions.
        Use this method to get the list of Indicator Sessions.
        """
        parameters = {}
        parameters['indicatorId'] = indicator_id
        return utils.read('Session', parameters)


@nsIndicator.route('/indicatortypes')
class IndicatorTypeList(Resource):
    mdIndicatorType = api_object.model(
        'IndicatorType',
        {'id': fields.Integer(required=False, description='Indicator type Id'),
            'name': fields.String(required=False, description='Indicator type name'),
            'module': fields.String(required=False, description='Indicator type module name'),
            'function': fields.String(required=False, description='Indicator type function name')})

    @nsIndicator.expect(api_object.models['IndicatorType'], validate=True)
    def post(self):
        """
        Create Indicator Type.
        Use this method to create an Indicator Type.
        """
        return utils.create('IndicatorType', request.json)

    def get(self):
        """
        Get list of Indicator Types.
        Use this method to get the list of Indicator Types.
        """
        return utils.read('IndicatorType')

    @nsIndicator.expect(api_object.models['IndicatorType'], validate=True)
    def put(self):
        """
        Update Indicator Type.
        Use this method to update an Indicator Type.
        """
        return utils.update('IndicatorType', request.json)

    @nsIndicator.expect(api_object.models['IndicatorType'], validate=True)
    def delete(self):
        """
        Delete Indicator Type.
        Use this method to delete an Indicator Type.
        """
        return utils.delete('IndicatorType', request.json)


# Status namespace
@nsStatus.route('/status')
class Status(Resource):
    """Class for Status API endpoints."""
    mdStatus = api_object.model(
        'Status',
        {'id': fields.Integer(required=False, description='Status Id'),
            'name': fields.String(required=False, description='Status name')})

    @nsStatus.expect(api_object.models['Status'], validate=True)
    def post(self):
        """
        Create Status.

        Use this method to create a Status.
        """
        return utils.create('Status', request.json)

    def get(self):
        """
        Get list of Status.

        Use this method to get the list of Status.
        """
        return utils.read('Status')

    @nsStatus.expect(api_object.models['Status'], validate=True)
    def put(self):
        """
        Update Status.

        Use this method to update a Status.
        """
        return utils.update('Status', request.json)

    @nsStatus.expect(api_object.models['Status'], validate=True)
    def delete(self):
        """
        Delete Status.

        Use this method to delete a Status.
        """
        return utils.delete('Status', request.json)


if __name__ == '__main__':
    config = Operation.get_parameter('api')
    app.run(host=config['host'], port=int(config['port']), threaded=True, debug=False)
