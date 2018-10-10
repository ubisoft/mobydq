import os
import urllib.parse as urlparse
import gdata
import json
from flask import redirect, request, jsonify, make_response, session
from flask_restplus import Namespace, Resource
from google_auth_oauthlib.flow import Flow
from security.token import get_jwt_token, TokenType


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


def get_user_email(oauth_token: str):
    user_client = gdata.client.GDClient()
    auth_token = gdata.gauth.AuthSubToken(oauth_token)
    response = user_client.request(
        'GET', 'https://www.googleapis.com/userinfo/v2/me', auth_token)
    j_obj = json.loads(response.read())
    return j_obj['email']


def register_google_oauth(namespace: Namespace):

    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class GoogleOAuth(Resource):

        def get(self):
            url, _ = flow.authorization_url()
            return redirect(url)

    @namespace.route('/security/oauth/google/callback')
    @namespace.doc()
    class GoogleOAuthCallback(Resource):

        def get(self):
            code = request.args.get('code')
            token = flow.fetch_token(code=code)
            resp = make_response(redirect(os.environ['AFTER_LOGIN_REDIRECT']))
            email = get_user_email(token['access_token'])
            jwt = get_jwt_token(TokenType.Google, email, token)
            resp.set_cookie('token', str(jwt))
            return resp
