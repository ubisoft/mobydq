#!/usr/bin/env python
"""Setup data quality framework database and perform CRUD operations."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import logging

from .base import Base, DictHelper

log = logging.getLogger(__name__)


class IndicatorType(Base, DictHelper):
    """Types of indicators."""

    __tablename__ = 'indicator_type'

    id = Column('indicator_type_id', Integer, primary_key=True)
    name = Column('indicator_type', String, nullable=False, unique=True)
    module = Column('module', String, nullable=False)
    function = Column('function', String, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicator = relationship('Indicator', backref='IndicatorType')


class Indicator(Base, DictHelper):
    """Data quality indicators."""

    __tablename__ = 'indicator'

    id = Column('indicator_id', Integer, primary_key=True)
    name = Column('indicator', String, nullable=False, unique=True)
    description = Column('indicator_description', String, nullable=False)
    indicatorTypeId = Column('indicator_type_id', Integer, ForeignKey('indicator_type.indicator_type_id'), nullable=False)
    batchOwnerId = Column('batch_owner_id', Integer, ForeignKey('batch_owner.batch_owner_id'), nullable=False)
    executionOrder = Column('execution_order', Integer, nullable=False, default=0)
    # alertOperator = Column('alert_operator', String, nullable=False) # This got moved to indicator parameters
    # alertThreshold = Column('alert_threshold', Float, nullable=False) # This got moved to indicator parameters
    # distributionList = Column('distribution_list', String, nullable=False) # This got moved to indicator parameters
    active = Column('flag_active', Boolean, nullable=False, default=True)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())

    indicatorParameter = relationship('IndicatorParameter', backref='Indicator', passive_deletes=True)
    indicatorResult = relationship('IndicatorResult', backref='Indicator', passive_deletes=True)
    session = relationship('Session', backref='Indicator', passive_deletes=True)


class IndicatorParameter(Base, DictHelper):
    """Indicator parameters."""

    __tablename__ = 'indicator_parameter'

    id = Column('indicator_parameter_id', Integer, primary_key=True)
    name = Column('indicator_parameter', String, nullable=False)
    value = Column('indicator_parameter_value', String, nullable=False)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
    updatedDate = Column('updated_date', DateTime, server_default=func.now(), onupdate=func.now())


class IndicatorResult(Base, DictHelper):
    """Indicator results."""

    __tablename__ = 'indicator_result'

    id = Column('indicator_result_id', Integer, primary_key=True)
    indicatorId = Column('indicator_id', Integer, ForeignKey('indicator.indicator_id', ondelete='CASCADE'), nullable=False)
    sessionId = Column('session_id', Integer, ForeignKey('session.session_id', ondelete='CASCADE'), nullable=False)
    alertOperator = Column('alert_operator', String, nullable=False)
    alertThreshold = Column('alert_threshold', Float, nullable=False)
    nbRecords = Column('nb_records', Integer, nullable=False)
    nbRecordsAlert = Column('nb_records_alert', Integer, nullable=False)
    nbRecordsNoAlert = Column('nb_records_no_alert', Integer, nullable=False)
    # This cannot be used for indicators with multiple measures
    # avgResult = Column('avg_result', Float, nullable=False)
    # This cannot be used for indicators with multiple measures
    # avgResultAlert = Column('avg_result_alert', Float, nullable=False)
    # This cannot be used for indicators with multiple measures
    # avgResultNoAlert = Column('avg_result_no_alert', Float, nullable=False)
    createdDate = Column('created_date', DateTime, server_default=func.now())
