from database.operation import Operation
import api_utils
import batch_schema
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateBatchInput(graphene.InputObjectType):
    """Input to create batch."""
    batchOwnerId = graphene.ID(required=True)
    statusId = graphene.ID(required=True)


class CreateBatch(graphene.Mutation):
    """Create batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = CreateBatchInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('Batch').create(**data)
        return CreateBatch(batch=batch)


class CreateBatchOwnerInput(graphene.InputObjectType):
    """Input to create batch owner."""
    name = graphene.String(required=True)


class CreateBatchOwner(graphene.Mutation):
    """Create batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(batch_schema.BatchOwner)

    class Arguments:
        input = CreateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('BatchOwner').create(**data)
        return CreateBatchOwner(batch_owner=batch_owner)


class ExecuteBatchInput(graphene.InputObjectType):
    """Input to execute batch."""
    batchOwnerId = graphene.ID(required=True)
    indicatorId = graphene.ID()


class ExecuteBatch(graphene.Mutation):
    """Execute batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = ExecuteBatchInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)

        # Start batch
        batch = Operation('Batch').create(batchOwnerId=data['batchOwnerId'], statusId=1)

        # Get indicators
        if 'indicatorId' in data.items():
            indicator_list = Operation('Indicator').read(id=data['indicatorId'], batchOwnerId=data['batchOwnerId'])
        else:
            indicator_list = Operation('Indicator').read(batchOwnerId=data['batchOwnerId'])

        # Execute indicators
        for indicator in indicator_list:
            # To be implemented
            # IndicatorMethod(indicator_record.id).execute(batch_record.id)
            print('Execute indicator: ' + indicator.name + ' in batch ' + str(batch.id))

        # Stop batch
        batch = Operation('Batch').update(id=batch.id, batchOwnerId=data['batchOwnerId'], statusId=2)  # Succeeded
        return ExecuteBatch(batch=batch)


class UpdateBatchInput(graphene.InputObjectType):
    """Input to update batch."""
    id = graphene.ID(required=True)
    batchOwnerId = graphene.ID()
    statusId = graphene.ID()


class UpdateBatch(graphene.Mutation):
    """Update batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = UpdateBatchInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('Batch').update(**data)
        return UpdateBatch(batch=batch)


class UpdateBatchInput(graphene.InputObjectType):
    """Input to update batch."""
    id = graphene.ID(required=True)
    batchOwnerId = graphene.ID()
    statusId = graphene.ID()


class UpdateBatchOwnerInput(graphene.InputObjectType):
    """Input to update batch."""
    id = graphene.ID(required=True)
    name = graphene.String(required=True)


class UpdateBatchOwner(graphene.Mutation):
    """Update batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(batch_schema.BatchOwner)

    class Arguments:
        input = UpdateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('BatchOwner').update(**data)
        return UpdateBatchOwner(batch_owner=batch_owner)
