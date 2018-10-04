from abc import ABC, abstractmethod
from flask import jsonify


class GraphQlRequestInterceptor(ABC):

    @abstractmethod
    def can_handle(self, ast):
        pass

    def intercept_ast_before_request(self, ast):
        return ast

    def after_request(self, executed_ast, status, response):
        return


class GraphQlRequestException(Exception):

    def __init__(self, code, message):
        self._code = code
        self._message = message

    def to_response(self):
        return jsonify(self._message), self._code
