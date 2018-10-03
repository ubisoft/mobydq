import graphql.utils as utils
from flask_restplus import Resource, fields
from flask import request, abort, jsonify
from graphql.batch import execute_batch
from graphql.data_source import test_data_source


def register_graphql(namespace, api):

    # Create expected headers and payload
    headers = api.parser()
    payload = api.model('Payload', {'query': fields.String(
        required=True,
        description='GraphQL query or mutation',
        example='{allIndicatorTypes{nodes{id,name}}}')})

    @namespace.route('/graphql', endpoint='with-parser')
    @namespace.doc()
    class GraphQL(Resource):

        @namespace.expect(headers, payload, validate=True)
        def post(self):
            """
            Execute GraphQL queries and mutations
            Use this endpoint to send http request to the GraphQL API.
            """
            payload = request.json

            # Execute request on GraphQL API
            status, data = utils.execute_graphql_request(payload['query'])

            # Execute batch of indicators
            if status == 200 and 'executeBatch' in payload['query']:
                if 'id' in data['data']['executeBatch']['batch']:
                    batch_id = str(data['data']['executeBatch']['batch']['id'])
                    execute_batch(batch_id)
                else:
                    message = 'Batch Id attribute is mandatory in the payload to be able to trigger the batch execution. Example: {"query": "mutation{executeBatch(input:{indicatorGroupId:1}){batch{id}}}"'
                    abort(400, message)

            # Test connectivity to a data source
            if status == 200 and 'testDataSource' in payload['query']:
                if 'id' in data['data']['testDataSource']['dataSource']:
                    data_source_id = str(
                        data['data']['testDataSource']['dataSource']['id'])
                    data = test_data_source(data_source_id)
                else:
                    message = "Data Source Id attribute is mandatory in the payload to be able to test the connectivity. Example: {'query': 'mutation{testDataSource(input:{dataSourceId:1}){dataSource{id}}}'"
                    abort(400, message)

            if status == 200:
                return jsonify(data)
            else:
                abort(500, data)
