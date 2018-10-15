import time
import os
from enum import Enum
from jwt import JWT
from jwt.exceptions import JWTDecodeError
from flask import make_response, redirect
from security.keys import get_private_key, get_public_key


TOKEN_VALIDITY = 3600


class TokenType(Enum):
    """Defines all OAuth providers"""
    Google = 0


def is_token_valid(token: str):
    """Checks whether a given JWT is valid"""
    verifying_key = get_public_key()
    try:
        parsed_token = JWT().decode(token, verifying_key)
        return int(parsed_token['exp']) > time.time()
    except JWTDecodeError:
        return False


def get_jwt_token(token_type: TokenType, email: str, user_info: object, oauth_token: object):
    """Gets a signed JWT token for the specified OAuth provider"""
    now = time.time()
    message = {
        'iss': os.environ['TOKEN_ISSUER'],
        'sub': email,
        'iat': now,
        'aud': 'postgraphile',
        'exp': now + TOKEN_VALIDITY,
        'type': str(token_type),
        'user_info': user_info,
        'user_token': oauth_token,
        'role': 'TBD for postgraphile',
        'user_id': 'TBD for postgraphile'
    }
    signing_key = get_private_key()
    return JWT().encode(message, signing_key, 'RS256')


def get_token_redirect_response(jwt: object):
    resp = make_response(redirect(os.environ['AFTER_LOGIN_REDIRECT']))
    resp.set_cookie('token', str(jwt))
    return resp
