#!/usr/bin/env python
"""Tables definitions for event objects."""
from .base import Base, Json, Dictionary
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class EventType(Base, Dictionary):
    """Types of events."""

    __tablename__ = 'event_type'

    id = Column('event_type_id', Integer, primary_key=True)
    name = Column('event_type', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='EventType')


class Event(Base, Dictionary):
    """Events."""

    __tablename__ = 'event'

    id = Column('event_id', Integer, primary_key=True)
    eventTypeId = Column('event_type_id', Integer, ForeignKey('event_type.event_type_id'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    content = Column('content', Json)
    createdDate = Column('created_date', DateTime, server_default=func.now())
