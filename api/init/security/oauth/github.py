import json
import os
from flask import redirect, request, session
from flask_restplus import Namespace, Resource
from requests_oauthlib import OAuth2Session
from security.token import get_jwt_token, TokenType, get_token_redirect_response

# pylint: disable=unused-variable

# OAuth endpoints given in the GitHub API documentation
AUTHORIZATION_URI = 'https://github.com/login/oauth/authorize'
TOKEN_URI = 'https://github.com/login/oauth/access_token'
USER_PROFILE_URI = 'https://api.github.com/user'
USER_EMAIL_URI = 'https://api.github.com/user/emails'
SCOPE = ['user:email']

# OAuth application configuration created on Github
client_id = os.environ['GITHUB_CLIENT_ID']
client_secret = os.environ['GITHUB_CLIENT_SECRET']
redirect_uri = os.environ['GITHUB_REDIRECT_URI']


def get_user_info(github_session: object):
    """Gets user profile using OAuth session."""

    user_profile = github_session.get(USER_PROFILE_URI).content.decode('utf-8')
    user_profile = json.loads(user_profile)

    if user_profile['email'] is None:
        emails = github_session.get(USER_EMAIL_URI).content.decode('utf-8')
        emails = json.loads(emails)
        user_profile['email'] = emails[0]['email']

    return user_profile


def register_github_oauth(namespace: Namespace):
    """Registers all endpoints used for Github OAuth authentication."""

    @namespace.route('/security/oauth/github')
    @namespace.doc()
    class GithubOAuth(Resource):
        """Defines resource to redirect user to Github OAuth page."""

        def get(self):
            """Redirects user to Github OAuth page."""

            github_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=SCOPE)
            url, state = github_session.authorization_url(AUTHORIZATION_URI)

            # State is used to prevent CSRF, keep this for later.
            session['oauth_state'] = state
            return redirect(url)

    @namespace.route('/security/oauth/github/callback')
    @namespace.doc()
    class GithubOAuthCallback(Resource):
        """Defines resource to handle callback from Github OAuth."""

        def get(self):
            """Handles Github OAuth callback and fetch user access token."""

            github_session = OAuth2Session(client_id, state=session['oauth_state'])
            token = github_session.fetch_token(TOKEN_URI, client_secret=client_secret, authorization_response=request.url)

            # Persist token in session
            # session['oauth_token'] = token

            user_info = get_user_info(github_session)
            jwt = get_jwt_token(TokenType.GITHUB, user_info['email'], user_info, token)
            return get_token_redirect_response(jwt)
