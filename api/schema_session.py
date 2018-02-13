from database.model_session import ModelSession
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeSession:
    """Generic class to provide descriptions of session attributes"""
    statusId = graphene.ID(description="Status Id of the session.")
    indicatorId = graphene.ID(description="Indicator Id of the session.")
    batchId = graphene.ID(description="Batch Id of the session.")


class SchemaSession(SQLAlchemyObjectType, AttributeSession):
    """Sessions."""
    class Meta:
        model = ModelSession
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
