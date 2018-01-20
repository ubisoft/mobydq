from graphene_sqlalchemy import SQLAlchemyObjectType
from database.status import Status as StatusModel
import graphene


class Status(SQLAlchemyObjectType):
    class Meta:
        model = StatusModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
