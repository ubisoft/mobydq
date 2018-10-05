import graphqlapi.utils as utils
from graphqlapi.proxy import proxy_request
from graphqlapi.interceptor import RequestException
from flask_restplus import Resource, fields, Namespace, Api
from docker.errors import APIError
from flask import request, abort, jsonify, make_response


def register_graphql(namespace: Namespace, api: Api):

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
            try:
                code, result = proxy_request(payload)
                return make_response(jsonify(result), code)
            except RequestException as ex:
                return ex.to_response()
            except APIError as apiError:
                return make_response(jsonify({'message': apiError.explanation}), apiError.status_code)
