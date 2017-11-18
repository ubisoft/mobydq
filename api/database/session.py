#!/usr/bin/env python
"""Tables definitions for session objects."""
from .base import Base, Dictionary
from .batch import BatchOwner, Batch
from .event import EventType, Event
from .indicator import IndicatorType, Indicator, IndicatorParameter, IndicatorResult
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Session(Base, Dictionary):
    """Sessions."""

    __tablename__ = 'session'

    id = Column('session_id', Integer, primary_key=True)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    batchId = Column('batch_id', Integer, ForeignKey('batch.batch_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship('Event', backref='Session', passive_deletes=True)
    indicatorResult = relationship('IndicatorResult', backref='Session', passive_deletes=True)
