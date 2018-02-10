from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_event import ModelEventType, ModelEvent
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class EventType(SQLAlchemyObjectType):
    """Types of events."""

    class Meta:
        model = ModelEventType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class Event(SQLAlchemyObjectType):
    """Events."""

    class Meta:
        model = ModelEvent
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
