#!/usr/bin/env python
"""Setup data quality framework database and perform CRUD operations."""
from .base import Base, Dictionary
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class BatchOwner(Base, Dictionary):
    """Batch owners."""

    __tablename__ = 'batch_owner'

    id = Column('batch_owner_id', Integer, primary_key=True)
    name = Column('batch_owner', String, nullable=False, unique=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    batch = relationship('Batch', backref='BatchOwner', passive_deletes=True)
    indicator = relationship('Indicator', backref='BatchOwner')


class Batch(Base, Dictionary):
    """Batches."""

    __tablename__ = 'batch'

    id = Column('batch_id', Integer, primary_key=True)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id', ondelete='CASCADE'), nullable=False)
    statusId = Column('status_id', Integer, ForeignKey('status.status_id'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    session = relationship('Session', backref='Batch', passive_deletes=True)
