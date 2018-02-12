from database.operation import Operation
from schema_session import AttributeSession, SchemaSession
import api_utils
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateSessionInput(graphene.InputObjectType, AttributeSession):
    """Arguments to create a session."""
    pass


class CreateSession(graphene.Mutation):
    """Mutation to create a session."""
    # Declare class attributes
    session = graphene.Field(SchemaSession)

    class Arguments:
        input = CreateSessionInput(required=True)

    def mutate(self, info, input):
        """Mutation to create a session."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        session = Operation('ModelSession').create(**data)
        return CreateSession(session=session)


class UpdateSessionInput(graphene.InputObjectType, AttributeSession):
    """Arguments to update a session."""
    id = graphene.ID(required=True)


class UpdateSession(graphene.Mutation):
    """Mutation to update a session."""
    # Declare class attributes
    session = graphene.Field(SchemaSession)

    class Arguments:
        input = UpdateSessionInput(required=True)

    def mutate(self, info, input):
        """Mutation to update a session."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        session = Operation('ModelSession').update(**data)
        return UpdateSession(session=session)
