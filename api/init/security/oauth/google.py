import json
import os
from flask import redirect, request, session
from flask_restplus import Namespace, Resource
from requests_oauthlib import OAuth2Session
from security.token import get_jwt_token, TokenType, get_token_redirect_response

# pylint: disable=unused-variable

# OAuth endpoints given in the Google API documentation
AUTHORIZATION_URI = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
USER_PROFILE_URI = 'https://www.googleapis.com/oauth2/v1/userinfo'
SCOPE = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

# OAuth application configuration created on Google
client_id = os.environ['GOOGLE_CLIENT_ID']
client_secret = os.environ['GOOGLE_CLIENT_SECRET']
redirect_uri = os.environ['HOST_NAME'] + '/mobydq/api/v1/security/oauth/google/callback'


def get_user_info(google_session: object):
    """Gets user profile using OAuth session."""

    user_profile = google_session.get(USER_PROFILE_URI).content.decode('utf-8')
    user_profile = json.loads(user_profile)

    return user_profile


def register_google_oauth(namespace: Namespace):
    """Registers all endpoints used for Google OAuth authentication."""

    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class GoogleOAuth(Resource):
        """Defines resource to redirect user to Google OAuth page."""

        def get(self):
            """Redirects user to Google OAuth page."""

            google_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=SCOPE)
            url, state = google_session.authorization_url(AUTHORIZATION_URI, access_type='offline', prompt='select_account')

            # State is used to prevent CSRF, keep this for later.
            session['oauth_state'] = state

            return redirect(url)

    @namespace.route('/security/oauth/google/callback')
    @namespace.doc()
    class GoogleOAuthCallback(Resource):
        """Defines resource to handle callback from Google OAuth."""

        def get(self):
            """Handles Google OAuth callback and fetch user access token."""

            google_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=SCOPE)
            token = google_session.fetch_token(TOKEN_URI, client_secret=client_secret, authorization_response=request.url)

            user_info = get_user_info(google_session)
            jwt = get_jwt_token(TokenType.GOOGLE, user_info['email'], user_info, token)
            return get_token_redirect_response(jwt)
