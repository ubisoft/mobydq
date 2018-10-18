import os
from flask import jsonify
from flask_restplus import Resource, Namespace

# pylint: disable=unused-variable
def register_health(namespace: Namespace):
    """Method used to register the health check namespace and endpoint."""

    @namespace.route('/health')
    @namespace.doc()
    class Health(Resource):
        def get(self):
            """
            Get API health status
            Use this endpoint to get the health status of this API.
            """
            is_debug = os.environ.get('FLASK_DEBUG')
            mode = 'debug' if is_debug else 'production'
            message = {'message': f'MobyDQ API running in {mode} mode'}

            return jsonify(message)
