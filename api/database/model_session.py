#!/usr/bin/env python
"""Tables definitions for session objects."""
from .base import Base, Dictionary
from .model_batch import ModelBatchOwner, ModelBatch
from .model_event import ModelEventType, ModelEvent
from .model_indicator import ModelIndicatorType, ModelIndicator, ModelIndicatorParameterType, ModelIndicatorParameter, ModelIndicatorResult
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ModelSession(Base, Dictionary):
    """Sessions."""

    __tablename__ = 'session'

    id = Column('session_id', Integer, primary_key=True)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    batchId = Column('batch_id', Integer, ForeignKey('batch.batch_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    events = relationship('ModelEvent', backref='session', passive_deletes=True)
    indicatorResults = relationship('ModelIndicatorResult', backref='session', passive_deletes=True)
