from graphene_sqlalchemy import SQLAlchemyObjectType
from database.batch import BatchOwner as BatchOwnerModel, Batch as BatchModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class BatchOwner(SQLAlchemyObjectType):
    """Batch owners."""

    class Meta:
        model = BatchOwnerModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class Batch(SQLAlchemyObjectType):
    """Batches."""

    class Meta:
        model = BatchModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
