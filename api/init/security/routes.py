from flask_restplus import Namespace, Resource, Api


def register_security(namespace: Namespace, api: Api):
    @namespace.route('/security')
    @namespace.doc()
    class Security(Resource):
        pass
