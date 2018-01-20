from graphene_sqlalchemy import SQLAlchemyObjectType
from database.session import Session as SessionModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
