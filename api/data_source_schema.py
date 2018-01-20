from graphene_sqlalchemy import SQLAlchemyObjectType
from database.data_source import DataSourceType as DataSourceTypeModel, DataSource as DataSourceModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class DataSourceType(SQLAlchemyObjectType):
    """Types of data sources."""

    class Meta:
        model = DataSourceTypeModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class DataSource(SQLAlchemyObjectType):
    """Data sources."""

    class Meta:
        model = DataSourceModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
