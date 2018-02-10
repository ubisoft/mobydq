from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_status import ModelStatus
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Status(SQLAlchemyObjectType):
    """Status for batches and sessions."""

    class Meta:
        model = ModelStatus
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
