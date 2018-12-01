import os
from flask import redirect, request, session
from flask.json import jsonify
from flask_restplus import Namespace, Resource
from requests_oauthlib import OAuth2Session
from security.token import get_jwt_token, TokenType, get_token_redirect_response


# OAuth endpoints given in the GitHub API documentation
github_authorization_uri = 'https://github.com/login/oauth/authorize'
github_token_uri = 'https://github.com/login/oauth/access_token'
github_user_profile_uri = 'https://api.github.com/user'

# OAuth application configuration created on Github
github_client_id = os.environ['GITHUB_CLIENT_ID']
github_client_secret = os.environ['GITHUB_CLIENT_SECRET']
github_redirect_uri = os.environ['GITHUB_REDIRECT_URI']


def get_user_info(token: str):
    """Gets user profile using OAuth token."""

    github = OAuth2Session(github_client_id, token=token)
    return jsonify(github.get(github_user_profile_uri).json())


def register_github_oauth(namespace: Namespace):
    """Registers all endpoints used for Github OAuth authentication"""

    @namespace.route('/security/oauth/github')
    @namespace.doc()
    class GithubOAuth(Resource):
        """Defines resource to redirect user to Github OAuth page."""

        def get(self):
            """Redirects user to Github OAuth page."""

            github = OAuth2Session(github_client_id)
            url, state = github.authorization_url(github_authorization_uri)

            # State is used to prevent CSRF, keep this for later.
            session['oauth_state'] = state
            return redirect(url)

    @namespace.route('/security/oauth/github/callback')
    @namespace.doc()
    class GithubOAuthCallback(Resource):
        """Defines resource to handle callback from Github OAuth."""

        def get(self):
            """Handles Github OAuth callback and fetch user access token."""

            github = OAuth2Session(github_client_id, state=session['oauth_state'])
            token = github.fetch_token(github_token_uri, client_secret=github_client_secret, authorization_response=request.url)

            # Persist token in session
            # session['oauth_token'] = token

            user_info = get_user_info(token)
            print(user_info)
            jwt = get_jwt_token(TokenType.Github, user_info['email'], user_info, token)
            return get_token_redirect_response(jwt)
