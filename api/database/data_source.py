#!/usr/bin/env python
"""Tables definitions for data source objects."""
from .base import Base, Dictionary
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class DataSourceType(Base, Dictionary):
    """Types of data sources."""

    __tablename__ = 'data_source_type'

    id = Column('data_source_type_id', Integer, primary_key=True)
    name = Column('data_source_type', String, nullable=False, unique=True)
    type = Column('data_source_parent_type', String, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    dataSources = relationship('DataSource', backref='DataSourceType')


class DataSource(Base, Dictionary):
    """Data sources."""

    __tablename__ = 'data_source'

    id = Column('data_source_id', Integer, primary_key=True)
    name = Column('data_source', String, nullable=False, unique=True)
    dataSourceTypeId = Column('data_source_type_id', Integer, ForeignKey('data_source_type.data_source_type_id'), nullable=False)
    connectionString = Column('connection_string', String)
    login = Column('login', String)
    password = Column('password', String)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())
