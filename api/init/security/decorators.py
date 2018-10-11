from flask import request, make_response, jsonify
from security.token import is_token_valid


AUTHORIZATION_HEADER = 'Authorization'
JWT_PREFIX = 'Bearer '


def token_required(func):

    def wrapper(*args, **kwargs):
        auth_header = _get_token_from_header()
        token = _parse_jwt_token(auth_header)
        unauthorized_response = make_response(jsonify({}), 401)
        if token is None:
            return unauthorized_response

        if not is_token_valid(token):
            return unauthorized_response

        return func(*args, **kwargs)
    return wrapper


def _get_token_from_header():
    if AUTHORIZATION_HEADER in request.headers:
        return request.headers[AUTHORIZATION_HEADER]
    return None


def _parse_jwt_token(auth_header: str):
    if auth_header is None:
        return None
    if auth_header.startswith(JWT_PREFIX):
        return auth_header.replace(JWT_PREFIX, '')
    return None
