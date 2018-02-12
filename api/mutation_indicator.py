from database.operation import Operation
from schema_indicator import AttributeIndicator, SchemaIndicator, AttributeIndicatorType, SchemaIndicatorType
from schema_indicator import AttributeIndicatorParameter, SchemaIndicatorParameter, AttributeIndicatorParameterType, SchemaIndicatorParameterType
from schema_indicator import AttributeIndicatorResult, SchemaIndicatorResult
import api_utils
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class CreateIndicatorInput(graphene.InputObjectType, AttributeIndicator):
    """Arguments to create an indicator."""
    pass


class CreateIndicator(graphene.Mutation):
    """Mutation to create an indicator."""
    # Declare class attributes
    indicator = graphene.Field(SchemaIndicator)

    class Arguments:
        input = CreateIndicatorInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an indicator."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator = Operation('ModelIndicator').create(**data)
        return CreateIndicator(indicator=indicator)


class CreateIndicatorParameterInput(graphene.InputObjectType, AttributeIndicatorParameter):
    """Arguments to create an indicator parameter."""
    pass


class CreateIndicatorParameter(graphene.Mutation):
    """Mutation to create an indicator parameter."""
    # Declare class attributes
    parameter = graphene.Field(SchemaIndicatorParameter)

    class Arguments:
        input = CreateIndicatorParameterInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an indicator parameter."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        parameter = Operation('ModelIndicatorParameter').create(**data)
        return CreateIndicatorParameter(parameter=parameter)


class CreateIndicatorParameterTypeInput(graphene.InputObjectType, AttributeIndicatorParameterType):
    """Arguments to create an indicator parameter type."""
    pass


class CreateIndicatorParameterType(graphene.Mutation):
    """Mutation to create an indicator parameter type."""
    # Declare class attributes
    parameter_type = graphene.Field(SchemaIndicatorParameterType)

    class Arguments:
        input = CreateIndicatorParameterTypeInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an indicator parameter type."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        parameter_type = Operation('ModelIndicatorParameterType').create(**data)
        return CreateIndicatorParameterType(parameter_type=parameter_type)


class CreateIndicatorResultInput(graphene.InputObjectType, AttributeIndicatorResult):
    """Arguments to create an indicator result summary."""
    pass


class CreateIndicatorResult(graphene.Mutation):
    """Mutation to create an indicator result summary."""
    # Declare class attributes
    indicator_result = graphene.Field(SchemaIndicatorResult)

    class Arguments:
        input = CreateIndicatorResultInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an indicator result summary."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator_result = Operation('ModelIndicatorResult').create(**data)
        return CreateIndicatorResult(indicator_result=indicator_result)


class CreateIndicatorTypeInput(graphene.InputObjectType, AttributeIndicatorType):
    """Arguments to create an indicator type."""
    pass


class CreateIndicatorType(graphene.Mutation):
    """Mutation to create an indicator type."""
    # Declare class attributes
    indicator_type = graphene.Field(SchemaIndicatorType)

    class Arguments:
        input = CreateIndicatorTypeInput(required=True)

    def mutate(self, info, input):
        """Mutation to create an indicator type."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator_type = Operation('ModelIndicatorType').create(**data)
        return CreateIndicatorType(indicator_type=indicator_type)


class UpdateIndicatorInput(graphene.InputObjectType, AttributeIndicator):
    """Arguments to update an indicator."""
    id = graphene.ID(required=True)


class UpdateIndicator(graphene.Mutation):
    """Mutation to update an indicator."""
    # Declare class attributes
    indicator = graphene.Field(SchemaIndicator)

    class Arguments:
        input = UpdateIndicatorInput(required=True)

    def mutate(self, info, input):
        """Mutation to update an indicator."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator = Operation('ModelIndicator').update(**data)
        return UpdateIndicator(indicator=indicator)


class UpdateIndicatorParameterInput(graphene.InputObjectType, AttributeIndicatorParameter):
    """Arguments to update an indicator parameter."""
    id = graphene.ID(required=True)


class UpdateIndicatorParameter(graphene.Mutation):
    """Mutation to update an indicator parameter."""
    # Declare class attributes
    parameter = graphene.Field(SchemaIndicatorParameter)

    class Arguments:
        input = UpdateIndicatorParameterInput(required=True)

    def mutate(self, info, input):
        """Mutation to update an indicator parameter."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        parameter = Operation('ModelIndicatorParameter').update(**data)
        return UpdateIndicatorParameter(parameter=parameter)


class UpdateIndicatorParameterTypeInput(graphene.InputObjectType, AttributeIndicatorParameterType):
    """Arguments to update an indicator parameter type."""
    id = graphene.ID(required=True)


class UpdateIndicatorParameterType(graphene.Mutation):
    """Mutation to update an indicator parameter type."""
    # Declare class attributes
    parameter_type = graphene.Field(SchemaIndicatorParameterType)

    class Arguments:
        input = UpdateIndicatorParameterTypeInput(required=True)

    def mutate(self, info, input):
        """Mutation to update an indicator parameter type."""
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        parameter_type = Operation('ModelIndicatorParameterType').update(**data)
        return UpdateIndicatorParameterType(parameter_type=parameter_type)


class UpdateIndicatorResultInput(graphene.InputObjectType, AttributeIndicatorResult):
    """Arguments to update an indicator result summary."""
    id = graphene.ID(required=True)


class UpdateIndicatorResult(graphene.Mutation):
    """Mutation to update an indicator result summary."""
    # Declare class attributes
    indicator_result = graphene.Field(SchemaIndicatorResult)

    class Arguments:
        input = UpdateIndicatorResultInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator_result = Operation('ModelIndicatorResult').update(**data)
        return UpdateIndicatorResult(indicator_result=indicator_result)


class UpdateIndicatorTypeInput(graphene.InputObjectType, AttributeIndicatorType):
    """Arguments to update an indicator type."""
    id = graphene.ID(required=True)


class UpdateIndicatorType(graphene.Mutation):
    """Mutation to update an indicator type."""
    # Declare class attributes
    indicator_type = graphene.Field(SchemaIndicatorType)

    class Arguments:
        input = UpdateIndicatorTypeInput(required=True)

    def mutate(self, info, input):
        # Convert input to dictionary
        data = api_utils.input_to_dictionary(input)
        indicator_type = Operation('ModelIndicatorType').update(**data)
        return UpdateIndicatorType(indicator_type=indicator_type)
