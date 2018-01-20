from graphene_sqlalchemy import SQLAlchemyObjectType
from database.event import EventType as EventTypeModel, Event as EventModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class EventType(SQLAlchemyObjectType):
    class Meta:
        model = EventTypeModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
