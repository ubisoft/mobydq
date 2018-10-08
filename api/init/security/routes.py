from flask_restplus import Namespace, Resource, Api


def register_security(namespace: Namespace, api: Api):
    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class Security(Resource):

        def get(self):
            pass
