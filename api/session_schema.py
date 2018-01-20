from graphene_sqlalchemy import SQLAlchemyObjectType
from database.session import Session as SessionModel
import graphene


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
