#!/usr/bin/env python
import json
import logging
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from base import Base, DictHelper

log = logging.getLogger(__name__)


class JsonEncodedDict(TypeDecorator):
    """Create sqlalchemy custom data type to enable json storage in event table."""

    impl = String

    def process_bind_param(self, value, dialect):
        """Dump."""
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        """Load."""
        return json.loads(value)


class Event(Base, DictHelper):
    """Events."""

    __tablename__ = 'event'

    id = Column('event_id', Integer, primary_key=True)
    eventTypeId = Column('event_type_id', Integer, ForeignKey('event_type.event_type_id'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    content = Column('content', JsonEncodedDict)
    createdDate = Column('created_date', DateTime, server_default=func.now())


class EventType(Base, DictHelper):
    """Types of events."""

    __tablename__ = 'event_type'

    id = Column('event_type_id', Integer, primary_key=True)
    name = Column('event_type', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='EventType')
