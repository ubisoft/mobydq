import os
import json
import requests
from flask import redirect, request, jsonify, make_response, session
from flask_restplus import Namespace, Resource
from google_auth_oauthlib.flow import Flow
from security.token import get_jwt_token, TokenType


google_redirect_url = os.environ['GOOGLE_REDIRECT_URI']
USER_PROFILE = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={}'
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


def get_user_info(oauth_token: str):
    request_url = USER_PROFILE.format(oauth_token)
    response = requests.get(request_url)
    return json.loads(response.text)


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
            user_info = get_user_info(token['access_token'])
            jwt = get_jwt_token(
                TokenType.Google, user_info['email'], user_info, token)
            resp.set_cookie('token', str(jwt))
            return resp
