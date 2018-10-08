from security.oauth.google import register_google_oauth
from flask_oauth import OAuth


def register_security(namespace: Namespace, api: Api):
    oauth = OAuth()
    register_google_oauth(oauth, namespace)
