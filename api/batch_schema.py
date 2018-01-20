from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay.node.node import from_global_id
from database.batch import BatchOwner as BatchOwnerModel, Batch as BatchModel
import api_utils
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


class CreateBatchOwner(graphene.Mutation):
    """Create batch owner."""

    class Arguments:
        name = graphene.String()

    # Class attributes
    ok = graphene.Boolean()
    batch_owner = graphene.Field(lambda: BatchOwner)

    def mutate(self, info, name):
        record = {'name': name}
        api_utils.create('BatchOwner', record)
        batch_owner = BatchOwner(name=name)
        ok = True
        return CreateBatchOwner(batch_owner=batch_owner, ok=ok)


class UpdateBatchOwner(graphene.Mutation):
    """Update batch owner."""

    class Arguments:
        id = graphene.String()
        name = graphene.String()

    # Class attributes
    ok = graphene.Boolean()
    batch_owner = graphene.Field(lambda: BatchOwner)

    def mutate(self, info, id, name):
        id = from_global_id(id)
        record = {'id': id[1], 'name': name}
        api_utils.update('BatchOwner', record)
        batch_owner = BatchOwner(id=id, name=name)
        ok = True
        return CreateBatchOwner(batch_owner=batch_owner, ok=ok)
