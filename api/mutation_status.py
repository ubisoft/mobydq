from database.operation import Operation
from schema_status import AttributeStatus, SchemaStatus
import api_utils
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateStatusInput(graphene.InputObjectType, AttributeStatus):
    """Arguments to create a status."""
    pass


class CreateStatus(graphene.Mutation):
    """Mutation to create a status."""
    # Declare class attributes
    status = graphene.Field(SchemaStatus)

    class Arguments:
        input = CreateStatusInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a status."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        status = Operation('ModelStatus').create(**data)
        return CreateStatus(status=status)


class UpdateStatusInput(graphene.InputObjectType, AttributeStatus):
    """Arguments to update a status."""
    id = graphene.ID(required=True)


class UpdateStatus(graphene.Mutation):
    """Mutation to update a status."""
    # Declare class attributes
    status = graphene.Field(SchemaStatus)

    class Arguments:
        input = UpdateStatusInput(required=True)

    def mutate(self, info, input):
        """Mutation to update a status."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        status = Operation('ModelStatus').update(**data)
        return UpdateStatus(status=status)
