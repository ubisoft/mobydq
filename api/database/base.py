#!/usr/bin/env python
import logging
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

log = logging.getLogger(__name__)

# Declarative base model to create database tables and classes
Base = declarative_base()


class DictHelper():
    def as_dict(self):
        result = {}
        for attr in self.__mapper__.columns.keys():
            value = getattr(self, attr)
            if isinstance(value, datetime):
                value = value.timestamp()
            result[attr] = value
        return result
