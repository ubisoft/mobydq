from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_indicator import ModelIndicatorType, ModelIndicator, ModelIndicatorParameter, ModelIndicatorResult
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class IndicatorType(SQLAlchemyObjectType):
    """Types of indicators."""

    class Meta:
        model = ModelIndicatorType
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure

    # name_hired_on = graphene.String()
    # def resolve_name_hired_on(self, info):
        # return '{} - {}'.format(self.name, str(self.hired_on))

    # @classmethod
    # def get_node(cls, info, id):
        # return print('employee id: ' + str(id))


class Indicator(SQLAlchemyObjectType):
    """Data quality indicators."""

    class Meta:
        model = ModelIndicator
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class IndicatorParameter(SQLAlchemyObjectType):
    """Indicator parameters."""

    class Meta:
        model = ModelIndicatorParameter
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class IndicatorResult(SQLAlchemyObjectType):
    """Indicator results."""

    class Meta:
        model = ModelIndicatorResult
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
