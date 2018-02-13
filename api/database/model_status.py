#!/usr/bin/env python
"""Tables definitions for status objects."""
from .base import Base, Dictionary
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ModelStatus(Base, Dictionary):
    """Status for batches and sessions."""

    __tablename__ = 'status'

    id = Column('status_id', Integer, primary_key=True)
    name = Column('status', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batches = relationship('ModelBatch', backref='status')
    sessions = relationship('ModelSession', backref='status')
