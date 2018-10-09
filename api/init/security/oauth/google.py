import os
import urllib.parse as urlparse
from flask import redirect, request, jsonify, make_response
from flask_restplus import Namespace, Resource
from google_auth_oauthlib.flow import Flow


google_redirect_url = os.environ['GOOGLE_REDIRECT_URI']
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

CLIENT_CONFIG = {
    'installed': {
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'redirect_uris': [google_redirect_url],
        'client_id': os.environ['GOOGLE_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_CLIENT_SECRET']
    }
}

flow = Flow.from_client_config(CLIENT_CONFIG, SCOPES)
flow.redirect_uri = google_redirect_url


def register_google_oauth(namespace: Namespace):

    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class GoogleOAuth(Resource):

        def get(self):
            url, state = flow.authorization_url()
            return redirect(url)

    @namespace.route('/security/oauth/google/callback')
    @namespace.doc()
    class GoogleOAuthCallback(Resource):

        def get(self):
            state = request.args.get('state')
            code = request.args.get('code')
            scope = request.args.get('scope')
            token = flow.fetch_token(code=code)
            resp = make_response(redirect(os.environ['AFTER_LOGIN_REDIRECT']))
            # create JWT token, return token in cookie
            resp.set_cookie('token', str(token))
            return resp
