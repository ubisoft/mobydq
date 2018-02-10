from database.operation import Operation
import api_utils
import schema_batch
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateBatchInput(graphene.InputObjectType, schema_batch.BatchAttribute):
    """Arguments to create a batch."""
    pass


class CreateBatch(graphene.Mutation):
    """Mutation to create a batch."""
    # Declare class attributes
    batch = graphene.Field(schema_batch.Batch)

    class Arguments:
        input = CreateBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('ModelBatch').create(**data)
        return CreateBatch(batch=batch)


class CreateBatchOwnerInput(graphene.InputObjectType, schema_batch.BatchOwnerAttribute):
    """Arguments to create a batch owner."""
    pass


class CreateBatchOwner(graphene.Mutation):
    """Mutation to create a batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(schema_batch.BatchOwner)

    class Arguments:
        input = CreateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a batch owner."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('ModelBatchOwner').create(**data)
        return CreateBatchOwner(batch_owner=batch_owner)


class ExecuteBatchInput(graphene.InputObjectType):
    """Arguments to execute a batch."""
    batchOwnerId = graphene.ID(required=True)
    indicatorId = graphene.ID()


class ExecuteBatch(graphene.Mutation):
    """Mutation to execute a batch."""
    # Declare class attributes
    batch = graphene.Field(schema_batch.Batch)

    class Arguments:
        input = ExecuteBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to execute a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = schema_batch.Batch.execute(**data)
        return ExecuteBatch(batch=batch)


class UpdateBatchInput(graphene.InputObjectType, schema_batch.BatchAttribute):
    """Arguments to update a batch."""
    id = graphene.ID(required=True)


class UpdateBatch(graphene.Mutation):
    """Mutation to update a batch."""
    # Declare class attributes
    batch = graphene.Field(schema_batch.Batch)

    class Arguments:
        input = UpdateBatchInput(required=True)

    def mutate(self, info, input):
        """Mutation to update a batch."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch = Operation('ModelBatch').update(**data)
        return UpdateBatch(batch=batch)


class UpdateBatchOwnerInput(graphene.InputObjectType, schema_batch.BatchOwnerAttribute):
    """Arguments to update a batch owner."""
    id = graphene.ID(required=True)


class UpdateBatchOwner(graphene.Mutation):
    """Mutation to update a batch owner."""
    # Declare class attributes
    batch_owner = graphene.Field(schema_batch.BatchOwner)

    class Arguments:
        input = UpdateBatchOwnerInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        batch_owner = Operation('ModelBatchOwner').update(**data)
        return UpdateBatchOwner(batch_owner=batch_owner)
