import time
import os
from enum import Enum
from jwt import JWT
from security.keys import get_private_key, get_public_key


TOKEN_VALIDITY = 3600


class TokenType(Enum):
    Google = 0


def get_jwt_token(token_type: TokenType, email: str, user_info: object, oauth_token: object):
    jwt = JWT()
    now = time.time()
    message = {
        'iss': os.environ['TOKEN_ISSUER'],
        'sub': email,
        'iat': now,
        'aud': 'postgraphile',
        'exp': now + TOKEN_VALIDITY,
        'user_info': user_info,
        'user_token': oauth_token,
        'role': 'TBD for postgraphile',
        'user_id': 'TBD for postgraphile'
    }
    signing_key = get_private_key()
    return jwt.encode(message, signing_key, 'RS256')
