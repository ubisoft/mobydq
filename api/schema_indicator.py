from database.model_indicator import ModelIndicatorType, ModelIndicator, ModelIndicatorParameterType, ModelIndicatorParameter, ModelIndicatorResult
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class AttributeIndicator:
    """Generic class to provide descriptions of indicator attributes"""
    name = graphene.String(description="Indicator name.")
    description = graphene.String(description="Indicator description.")
    indicatorTypeId = graphene.ID(description="Indicator type Id of the indicator.")
    batchOwnerId = graphene.ID(description="Batch owner Id of the indicator.")
    executionOrder = graphene.Int(description="Order of execution of the indicator when it is executed in a batch with several other indicators.")
    active = graphene.Boolean(description="Indicates if the indicator is active or inactive. Only active indicators can be executed.")


class SchemaIndicator(SQLAlchemyObjectType, AttributeIndicator):
    """Data quality indicators."""
    class Meta:
        model = ModelIndicator
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeIndicatorParameter:
    """Generic class to provide descriptions of indicator parameter attributes"""
    indicatorId = graphene.ID(description="Indicator Id of the parameter.")
    parameterTypeId = graphene.String(description="Parameter type Id of the parameter.")
    value = graphene.String(description="Value of the parameter.")


class SchemaIndicatorParameter(SQLAlchemyObjectType, AttributeIndicatorParameter):
    """Indicator parameters."""
    class Meta:
        model = ModelIndicatorParameter
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeIndicatorParameterType:
    """Generic class to provide descriptions of indicator parameter type attributes"""
    name = graphene.String(description="Parameter type name.")
    description = graphene.String(description="Parameter type description.")


class SchemaIndicatorParameterType(SQLAlchemyObjectType, AttributeIndicatorParameterType):
    """Indicator parameter types."""
    class Meta:
        model = ModelIndicatorParameterType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeIndicatorResult:
    """Generic class to provide descriptions of indicator result attributes"""
    indicatorId = graphene.ID(description="Indicator Id of the results set.")
    sessionId = graphene.ID(description="Session Id of the result set.")
    alertOperator = graphene.String(description="Alert operator used during the execution of the indicator.")
    alertThreshold = graphene.Float(description="Alert threshold used during the execution of the indicator.")
    nbRecords = graphene.Int(description="Number of records in the result set.")
    nbRecordsAlert = graphene.Int(description="Number of records which triggered an alert in the result set.")
    nbRecordsNoAlert = graphene.Int(description="Number of records which did not trigger an alert in the result set.")


class SchemaIndicatorResult(SQLAlchemyObjectType, AttributeIndicatorResult):
    """Indicator results."""
    class Meta:
        model = ModelIndicatorResult
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class AttributeIndicatorType:
    """Generic class to provide descriptions of indicator type attributes"""
    name = graphene.String(description="Indicator type name.")
    function = graphene.String(description="Python function of the framework used to compute this indicator type.")


class SchemaIndicatorType(SQLAlchemyObjectType, AttributeIndicatorType):
    """Types of indicators."""
    class Meta:
        model = ModelIndicatorType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
