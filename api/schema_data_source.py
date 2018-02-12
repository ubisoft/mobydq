from database.model_data_source import ModelDataSourceType, ModelDataSource
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeDataSource:
    """Generic class to provide descriptions of data source attributes"""
    name = graphene.String(description="Data source name.")
    dataSourceTypeId = graphene.ID(description="Data source type Id of the data source.")
    connectionString = graphene.ID(description="Connection string used to connect to the data source.")
    login = graphene.ID(description="Login used to connect to the data source.")
    password = graphene.ID(description="Password used to connect to the data source.")


class SchemaDataSource(SQLAlchemyObjectType, AttributeDataSource):
    """Data sources."""
    class Meta:
        model = ModelDataSource
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeDataSourceType:
    """Generic class to provide descriptions of data source type attributes"""
    name = graphene.String(description="Data source type name.")
    parentType = graphene.String(description="Parent type of the data source type.")


class SchemaDataSourceType(SQLAlchemyObjectType, AttributeDataSourceType):
    """Types of data sources."""
    class Meta:
        model = ModelDataSourceType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
