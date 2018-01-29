from database.operation import Operation
import api_utils
import batch_schema
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateBatchInput(graphene.InputObjectType):
    """Arguments to create a batch."""
    batchOwnerId = graphene.ID(required=True)
    statusId = graphene.ID(required=True)


class CreateBatch(graphene.Mutation):
    """Mutation to create a batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = CreateBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('Batch').create(**data)
        return CreateBatch(batch=batch)


class CreateBatchOwnerInput(graphene.InputObjectType):
    """Arguments to create a batch owner."""
    name = graphene.String(required=True)


class CreateBatchOwner(graphene.Mutation):
    """Mutation to create a batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(batch_schema.BatchOwner)

    class Arguments:
        input = CreateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a batch owner."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('BatchOwner').create(**data)
        return CreateBatchOwner(batch_owner=batch_owner)


class ExecuteBatchInput(graphene.InputObjectType):
    """Arguments to execute a batch."""
    batchOwnerId = graphene.ID(required=True)
    indicatorId = graphene.ID()


class ExecuteBatch(graphene.Mutation):
    """Mutation to execute a batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = ExecuteBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to execute a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = batch_schema.Batch.execute(**data)
        return ExecuteBatch(batch=batch)


class UpdateBatchInput(graphene.InputObjectType):
    """Arguments to update a batch."""
    id = graphene.ID(required=True)
    batchOwnerId = graphene.ID()
    statusId = graphene.ID()


class UpdateBatch(graphene.Mutation):
    """Mutation to update a batch."""
    # Declare class attributes
    batch = graphene.Field(batch_schema.Batch)

    class Arguments:
        input = UpdateBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to update a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('Batch').update(**data)
        return UpdateBatch(batch=batch)


class UpdateBatchOwnerInput(graphene.InputObjectType):
    """Arguments to update a batch owner."""
    id = graphene.ID(required=True)
    name = graphene.String(required=True)


class UpdateBatchOwner(graphene.Mutation):
    """Mutation to update a batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(batch_schema.BatchOwner)

    class Arguments:
        input = UpdateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('BatchOwner').update(**data)
        return UpdateBatchOwner(batch_owner=batch_owner)
