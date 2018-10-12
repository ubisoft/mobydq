import os
import json
import requests
from flask import redirect, request, jsonify, make_response, session
from flask_restplus import Namespace, Resource
from google_auth_oauthlib.flow import Flow
from security.token import get_jwt_token, TokenType, get_token_redirect_response

# pylint: disable=unused-variable


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

# Create an OAuth flow (Authorization Code) from client id and client secret
flow = Flow.from_client_config(CLIENT_CONFIG, SCOPES)
# Redirect the user back after login
flow.redirect_uri = google_redirect_url


def get_user_info(oauth_token: str):
    """Gets the user profile of the user after login using the corresponding OAuth token"""
    request_url = USER_PROFILE.format(oauth_token)
    response = requests.get(request_url)
    return json.loads(response.text)


def register_google_oauth(namespace: Namespace):
    """Registers all endpoints used for Google OAuth authentication"""

    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class GoogleOAuth(Resource):
        """Defines the resource to redirect the user to the Google OAuth page"""

        def get(self):
            """Redirects the user to the Google OAuth page"""
            url, _ = flow.authorization_url()
            return redirect(url)

    @namespace.route('/security/oauth/google/callback')
    @namespace.doc()
    class GoogleOAuthCallback(Resource):
        """Defines the resource to handle the callback from Google OAuth"""

        def get(self):
            """Handles the Google OAuth callback and returns the token in the cookie"""
            code = request.args.get('code')
            token = flow.fetch_token(code=code)
            user_info = get_user_info(token['access_token'])
            jwt = get_jwt_token(
                TokenType.Google, user_info['email'], user_info, token)
            return get_token_redirect_response(jwt)
