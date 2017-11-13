import logging
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from base import Base, DictHelper

log = logging.getLogger(__name__)


class Session(Base, DictHelper):
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
