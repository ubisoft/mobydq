from flask_restplus import Namespace, Api
from security.oauth.google import register_google_oauth


def register_security(namespace: Namespace, api: Api):
    register_google_oauth(namespace)
