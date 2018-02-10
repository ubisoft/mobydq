from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_session import ModelSession
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Session(SQLAlchemyObjectType):
    """Sessions."""

    class Meta:
        model = ModelSession
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
