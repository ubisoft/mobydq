#!/usr/bin/env python
"""Setup data quality framework database and perform CRUD operations."""
from .base import Base, Dictionary
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Status(Base, Dictionary):
    """Status for batches and sessions."""

    __tablename__ = 'status'

    id = Column('status_id', Integer, primary_key=True)
    name = Column('status', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='Status')
    session = relationship('Session', backref='Status')
