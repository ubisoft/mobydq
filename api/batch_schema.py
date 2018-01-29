from database.operation import Operation
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

    @staticmethod
    def execute(**kwargs):
        """
        Execute batch.
        Expected keyword arguments are batchOwnerId and indicatorId
        """
        # Start batch
        batch = Operation('Batch').create(batchOwnerId=kwargs['batchOwnerId'], statusId=1)

        # Get indicators for corresponding batch owner
        if 'indicatorId' in kwargs.items():
            indicator_list = Operation('Indicator').read(id=kwargs['indicatorId'], batchOwnerId=kwargs['batchOwnerId'])
        else:
            indicator_list = Operation('Indicator').read(batchOwnerId=kwargs['batchOwnerId'])

        # Execute indicators
        for indicator in indicator_list:
            # To be implemented
            # IndicatorMethod(indicator_record.id).execute(batch_record.id)
            print('Execute indicator: ' + indicator.name + ' in batch ' + str(batch.id))

        # Stop batch
        batch = Operation('Batch').update(id=batch.id, batchOwnerId=kwargs['batchOwnerId'], statusId=2)
        return batch
