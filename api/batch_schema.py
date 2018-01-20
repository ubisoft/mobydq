from graphene_sqlalchemy import SQLAlchemyObjectType
from database.batch import BatchOwner as BatchOwnerModel, Batch as BatchModel
import graphene


class BatchOwner(SQLAlchemyObjectType):
    class Meta:
        model = BatchOwnerModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class Batch(SQLAlchemyObjectType):
    class Meta:
        model = BatchModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
