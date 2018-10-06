from flask import jsonify, make_response


class RequestException(Exception):
    """Method to manage errors when sending http request to GraphQL."""

    def __init__(self, status: int, response: object):
        self._status = status
        if type(response) == str:
            response = {'message': response}
        self._response = response

    def to_response(self):
        return make_response(jsonify(self._response), self._status)
