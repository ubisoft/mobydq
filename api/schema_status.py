from database.model_status import ModelStatus
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeStatus:
    """Generic class to provide descriptions of status attributes"""
    name = graphene.String(description="Status name.")


class SchemaStatus(SQLAlchemyObjectType, AttributeStatus):
    """Status for batches and sessions."""
    class Meta:
        model = ModelStatus
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
