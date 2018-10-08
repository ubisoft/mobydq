import os
import urllib.parse as urlparse
from flask_oauth import OAuth, OAuthRemoteApp
from flask_restplus import Namespace, Resource


def register_google_oauth(oauth: OAuth, namespace: Namespace):
    google_app = get_google_app(oauth)
    google_redirect_uri = os.environ['GOOGLE_REDIRECT_URI']

    @namespace.route('/security/oauth/google')
    @namespace.doc()
    class GoogleOAuth(Resource):

        def get(self):
            pass

    @namespace.route(google_redirect_uri)
    @namespace.doc()
    @google_app.authorized_handler
    class GoogleOAuthCallback(Resource):

        def post(self, response):
            pass


def get_google_app(oauth: OAuth):
    client_id = os.environ['GOOGLE_CLIENT_ID']
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    google_remote_app = oauth.remote_app('google',
                                         base_url='https://www.google.com/accounts/',
                                         authorize_url='https://accounts.google.com/o/oauth2/auth',
                                         request_token_url=None,
                                         request_token_params={
                                             'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                                             'response_type': 'code'
                                         },
                                         access_token_url='https://accounts.google.com/o/oauth2/token',
                                         access_token_method='POST',
                                         access_token_params={
                                             'grant_type': 'authorization_code'
                                         },
                                         consumer_key=client_id,
                                         consumer_secret=client_secret)
    return google_remote_app
