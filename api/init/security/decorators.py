from flask import request, make_response, jsonify
from security.token import is_token_valid


AUTHORIZATION_HEADER = 'Authorization'
JWT_PREFIX = 'Bearer '


def token_required(func):
    """
    Gets a decorator to check whether a valid token is in the request headers.
    It will return 401, if the user provdies an invalid token.
    """
    def wrapper(*args, **kwargs):
        auth_header = _get_token_from_header()
        token = _parse_jwt_token(auth_header)
        unauthorized_response = make_response(
            jsonify({'message': 'Unauthorized'}), 401)
        if token is None:
            return unauthorized_response

        if not is_token_valid(token):
            return unauthorized_response

        return func(*args, **kwargs)
    return wrapper


def _get_token_from_header():
    """Gets the JWT token from the HTTP headers"""
    if AUTHORIZATION_HEADER in request.headers:
        return request.headers[AUTHORIZATION_HEADER]
    return None


def _parse_jwt_token(auth_header: str):
    """Parses the JWT token from the Authorization header"""
    if auth_header is None:
        return None
    if auth_header.startswith(JWT_PREFIX):
        return auth_header.replace(JWT_PREFIX, '')
    return None
