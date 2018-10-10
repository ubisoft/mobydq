from enum import Enum
from jwt import JWT, jwk_from_dict, jwk_from_pem


class TokenType(Enum):
    Google = 0


def get_jwt_token(token_type: TokenType, email: str, oauth_token: object):
    jwt = JWT()
    message = {
        'tok': oauth_token,
        'iss': 'https://example.com/',
        'sub': 'yosida95',
        'iat': 1485969205,
        'exp': 1485972800
    }
    return jwt.encode(message, None, 'RS256')
