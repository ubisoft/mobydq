from graphene_sqlalchemy import SQLAlchemyObjectType
from database.status import Status as StatusModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Status(SQLAlchemyObjectType):
    """Status for batches and sessions."""

    class Meta:
        model = StatusModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
