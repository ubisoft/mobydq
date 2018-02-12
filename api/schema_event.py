from database.model_event import ModelEventType, ModelEvent
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeEvent:
    """Generic class to provide descriptions of event attributes"""
    eventTypeId = graphene.ID(description="Event type Id of the event.")
    sessionId = graphene.ID(description="Session Id of the event.")


class SchemaEvent(SQLAlchemyObjectType, AttributeEvent):
    """Events."""
    class Meta:
        model = ModelEvent
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeEventType:
    """Generic class to provide descriptions of event type attributes"""
    name = graphene.String(description="Event type name.")


class SchemaEventType(SQLAlchemyObjectType, AttributeEventType):
    """Types of events."""
    class Meta:
        model = ModelEventType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
