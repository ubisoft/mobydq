from flask_restplus import Namespace
from security.oauth.github import register_github_oauth
from security.oauth.google import register_google_oauth


def register_security(namespace: Namespace):
    """Registers all resources for the security module"""
    register_github_oauth(namespace)
    register_google_oauth(namespace)
