from graphql_relay.node.node import from_global_id, to_global_id
import api_utils
import batch_schema
import graphene
import logging
import status_schema

# Load logging configuration
log = logging.getLogger(__name__)


class CreateBatchInput(graphene.InputObjectType):
    """Input to create batch."""
    batchOwnerId = graphene.String(required=True)
    statusId = graphene.String(required=True)


class CreateBatch(graphene.Mutation):
    """Create batch."""
    class Arguments:
        input = CreateBatchInput(required=True)

    # Class attributes
    batch = graphene.Field(lambda: batch_schema.Batch)

    @staticmethod
    def mutate(root, info, input=None):
        """Method to create batch."""
        # Convert input to dictionary
        record = {}
        for key in input:
            if key[-2:].lower() == 'id':
                input[key] = from_global_id(input[key])[1]  # Convert global id to database id
            record[key] = input[key]
        batch = api_utils.create('Batch', record)
        batch['id'] = to_global_id('Batch', batch['id'])
        batch = batch_schema.Batch(**batch)
        return CreateBatch(batch=batch)


class CreateBatchOwnerInput(graphene.InputObjectType):
    """Input to create batch owner."""
    name = graphene.String(required=True)


class CreateBatchOwner(graphene.Mutation):
    """Create batch owner."""
    class Arguments:
        input = CreateBatchOwnerInput(required=True)

    # Class attributes
    batch_owner = graphene.Field(lambda: batch_schema.BatchOwner)

    @staticmethod
    def mutate(root, info, input=None):
        """Method to create batch owner."""
        # Convert input to dictionary
        record = {}
        for key in input:
            if key[-2:].lower() == 'id':
                input[key] = from_global_id(input[key])[1]  # Convert global id to database id
            record[key] = input[key]
        batch_owner = api_utils.create('BatchOwner', record)
        batch_owner = batch_schema.BatchOwner(**batch_owner)
        batch_owner.id = to_global_id('BatchOwner', batch_owner.id)
        return CreateBatchOwner(batch_owner=batch_owner)


class UpdateBatchInput(graphene.InputObjectType):
    """Input to update batch."""
    id = graphene.ID(required=True)
    batchOwnerId = graphene.String()
    statusId = graphene.String()


class UpdateBatch(graphene.Mutation):
    """Update batch."""
    class Arguments:
        input = UpdateBatchInput(required=True)

    # Class attributes
    batch = graphene.Field(lambda: batch_schema.Batch)
    batch_owner = graphene.Field(lambda: batch_schema.BatchOwner)
    status = graphene.Field(lambda: status_schema.Status)

    @staticmethod
    def mutate(self, info, input):
        record = {}
        for key in input:
            if key[-2:].lower() == 'id':
                input[key] = from_global_id(input[key])[1]  # Convert global id to database id
            record[key] = input[key]

        batch = api_utils.update('Batch', record)
        batch = batch_schema.Batch(**batch)

        batch_owner = None
        if 'batchOwnerId' in record:
            batch_owner = api_utils.read('BatchOwner', {'id': record['batchOwnerId']})
            batch_owner = batch_schema.BatchOwner(**batch_owner[0])

        status = None
        if 'statusId' in record:
            status = api_utils.read('Status', {'id': record['statusId']})
            status = status_schema.Status(**status[0])

        return UpdateBatch(batch=batch, batch_owner=batch_owner, status=status)


class UpdateBatchOwnerInput(graphene.InputObjectType):
    """Input to update batch owner."""
    id = graphene.ID(required=True)
    name = graphene.String()


class UpdateBatchOwner(graphene.Mutation):
    """Update batch owner."""
    class Arguments:
        input = UpdateBatchOwnerInput(required=True)

    # Class attributes
    batch_owner = graphene.Field(lambda: batch_schema.BatchOwner)

    @staticmethod
    def mutate(self, info, input):
        # Convert input to dictionary
        record = {}
        for key in input:
            if key[-2:].lower() == 'id':
                input[key] = from_global_id(input[key])[1]  # Convert global id to database id
            record[key] = input[key]
        batch_owner = api_utils.update('BatchOwner', record)
        batch_owner = batch_schema.BatchOwner(**batch_owner)
        return UpdateBatchOwner(batch_owner)
