from database.operation import Operation
from schema_data_source import AttributeDataSource, SchemaDataSource, AttributeDataSourceType, SchemaDataSourceType
import api_utils
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateDataSourceInput(graphene.InputObjectType, AttributeDataSource):
    """Arguments to create a data source."""
    pass


class CreateDataSource(graphene.Mutation):
    """Mutation to create a data source."""
    # Declare class attributes
    data_source = graphene.Field(SchemaDataSource)

    class Arguments:
        input = CreateDataSourceInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a data source."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        data_source = Operation('ModelDataSource').create(**data)
        return CreateDataSource(data_source=data_source)


class CreateDataSourceTypeInput(graphene.InputObjectType, AttributeDataSourceType):
    """Arguments to create a data source type."""
    pass


class CreateDataSourceType(graphene.Mutation):
    """Mutation to create a data source type."""
    # Declare class attributes
    data_source_type = graphene.Field(SchemaDataSourceType)

    class Arguments:
        input = CreateDataSourceTypeInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a data source type."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        data_source_type = Operation('ModelDataSourceType').create(**data)
        return CreateDataSourceType(data_source_type=data_source_type)


class UpdateDataSourceInput(graphene.InputObjectType, AttributeDataSource):
    """Arguments to update a data source."""
    id = graphene.ID(required=True)


class UpdateDataSource(graphene.Mutation):
    """Mutation to update a data source."""
    # Declare class attributes
    data_source = graphene.Field(SchemaDataSource)

    class Arguments:
        input = UpdateDataSourceInput(required=True)

    def mutate(self, info, input):
        """Mutation to update a data source."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        data_source = Operation('ModelDataSource').update(**data)
        return UpdateDataSource(data_source=data_source)


class UpdateDataSourceTypeInput(graphene.InputObjectType, AttributeDataSourceType):
    """Arguments to update a data source type."""
    id = graphene.ID(required=True)


class UpdateDataSourceType(graphene.Mutation):
    """Mutation to update a data source type."""
    # Declare class attributes
    data_source_type = graphene.Field(SchemaDataSourceType)

    class Arguments:
        input = UpdateDataSourceTypeInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        data_source_type = Operation('ModelDataSourceType').update(**data)
        return UpdateDataSourceType(data_source_type=data_source_type)
