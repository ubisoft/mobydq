from database.operation import Operation
from schema_event import AttributeEvent, SchemaEvent, AttributeEventType, SchemaEventType
import api_utils
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateEventInput(graphene.InputObjectType, AttributeEvent):
    """Arguments to create an event."""
    pass


class CreateEvent(graphene.Mutation):
    """Mutation to create an event."""
    # Declare class attributes
    event = graphene.Field(SchemaEvent)

    class Arguments:
        input = CreateEventInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an event."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        event = Operation('ModelEvent').create(**data)
        return CreateEvent(event=event)


class CreateEventTypeInput(graphene.InputObjectType, AttributeEventType):
    """Arguments to create an event type."""
    pass


class CreateEventType(graphene.Mutation):
    """Mutation to create an event type."""
    # Declare class attributes
    event_type = graphene.Field(SchemaEventType)

    class Arguments:
        input = CreateEventTypeInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an event type."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        event_type = Operation('ModelEventType').create(**data)
        return CreateEventType(event_type=event_type)


class UpdateEventInput(graphene.InputObjectType, AttributeEvent):
    """Arguments to update an event."""
    id = graphene.ID(required=True)


class UpdateEvent(graphene.Mutation):
    """Mutation to update an event."""
    # Declare class attributes
    event = graphene.Field(SchemaEvent)

    class Arguments:
        input = UpdateEventInput(required=True)

    def mutate(self, info, input):
        """Mutation to update an event."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        event = Operation('ModelEvent').update(**data)
        return UpdateEvent(event=event)


class UpdateEventTypeInput(graphene.InputObjectType, AttributeEventType):
    """Arguments to update an event type."""
    id = graphene.ID(required=True)


class UpdateEventType(graphene.Mutation):
    """Mutation to update a data source type."""
    # Declare class attributes
    event_type = graphene.Field(SchemaEventType)

    class Arguments:
        input = UpdateEventTypeInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        event_type = Operation('ModelEventType').update(**data)
        return UpdateEventType(event_type=event_type)
