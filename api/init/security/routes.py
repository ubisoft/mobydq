from flask_restplus import Namespace
from security.oauth.google import register_google_oauth


def register_security(namespace: Namespace):
    """Registers all resources for the security module"""
    register_google_oauth(namespace)
