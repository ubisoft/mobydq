from database.model_batch import ModelBatchOwner, ModelBatch
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeBatch:
    """Generic class to provide descriptions of batch attributes"""
    batchOwnerId = graphene.ID(description="Batch owner Id of the batch.")
    statusId = graphene.ID(description="Status Id of the batch.")


class SchemaBatch(SQLAlchemyObjectType, AttributeBatch):
    """Batches."""
    class Meta:
        model = ModelBatch
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeBatchOwner:
    """Generic class to provide descriptions of batch owner attributes"""
    name = graphene.String(description="Batch owner name.")


class SchemaBatchOwner(SQLAlchemyObjectType, AttributeBatchOwner):
    """Batch owners."""
    class Meta:
        model = ModelBatchOwner
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
