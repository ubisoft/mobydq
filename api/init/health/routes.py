import os
from flask_restplus import Resource
from flask import jsonify


def register_health(namespace):
    @namespace.route('/health')
    @namespace.doc()
    class Health(Resource):
        def get(self):
            """
            Get API health status
            Use this endpoint to get the health status of this API.
            """
            is_debug = os.environ.get('FLASK_DEBUG')
            mode = 'production' if not is_debug else 'debug'
            message = {
                'message': f'MobyDQ API running in {mode} mode'
            }

            return jsonify(message)
