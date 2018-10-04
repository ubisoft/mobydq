from abc import ABC, abstractmethod
from flask import jsonify
from graphql.language.ast import Document


class GraphQlRequestInterceptor(ABC):

    @abstractmethod
    def can_handle(self, ast: Document):
        pass

    def intercept_ast_before_request(self, ast: Document):
        return ast

    def after_request(self, executed_ast: Document, status: int, response: object):
        return response


class GraphQlRequestException(Exception):

    def __init__(self, code: int, message: object):
        self._code = code
        self._message = message

    def to_response(self):
        return jsonify(self._message), self._code
