from graphene_sqlalchemy import SQLAlchemyObjectType
from database.indicator import IndicatorType as IndicatorTypeModel, Indicator as IndicatorModel
from database.indicator import IndicatorParameter as IndicatorParameterModel, IndicatorResult as IndicatorResultModel
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class IndicatorType(SQLAlchemyObjectType):
    """Types of indicators."""

    class Meta:
        model = IndicatorTypeModel
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
        model = IndicatorModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class IndicatorParameter(SQLAlchemyObjectType):
    """Indicator parameters."""

    class Meta:
        model = IndicatorParameterModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure


class IndicatorResult(SQLAlchemyObjectType):
    """Indicator results."""

    class Meta:
        model = IndicatorResultModel
        interfaces = (graphene.relay.Node,)  # Keep comma to avoid failure
