from flask import jsonify, make_response


class RequestException(Exception):

    def __init__(self, code: int, message: object):
        self._code = code
        if type(message) == str:
            message = {'message': message}
        self._message = message

    def to_response(self):
        return make_response(jsonify(self._message), self._code)
