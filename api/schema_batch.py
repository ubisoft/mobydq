from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_batch import ModelBatchOwner, ModelBatch
from database.operation import Operation
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class BatchOwnerAttribute:
    """Generic class to provide descriptions of batch owner attributes"""
    name = graphene.String(description="Batch owner name.")


class BatchOwner(SQLAlchemyObjectType, BatchOwnerAttribute):
    """Batch owners."""

    class Meta:
        model = ModelBatchOwner
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class BatchAttribute:
    """Generic class to provide descriptions of batch attributes"""
    batchOwnerId = graphene.ID(description="Batch owner Id of the batch.")
    statusId = graphene.ID(description="Status Id of the batch.")


class Batch(SQLAlchemyObjectType, BatchAttribute):
    """Batches."""

    class Meta:
        model = ModelBatch
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure

    @staticmethod
    def execute(**kwargs):
        """Execute a batch of indicators for the corresponding batch owner"""
        # Start batch
        batch = Operation('ModelBatch').create(batchOwnerId=kwargs['batchOwnerId'], statusId=1)

        # Get indicators for corresponding batch owner
        if 'indicatorId' in kwargs.items():
            indicator_list = Operation('ModelIndicator').read(id=kwargs['indicatorId'], batchOwnerId=kwargs['batchOwnerId'])
        else:
            indicator_list = Operation('ModelIndicator').read(batchOwnerId=kwargs['batchOwnerId'])

        # Execute indicators
        for indicator in indicator_list:
            # To be implemented
            # IndicatorMethod(indicator_record.id).execute(batch_record.id)
            print('Execute indicator: ' + indicator.name + ' in batch ' + str(batch.id))

        # Stop batch
        batch = Operation('ModelBatch').update(id=batch.id, batchOwnerId=kwargs['batchOwnerId'], statusId=2)
        return batch
