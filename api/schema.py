from graphene_sqlalchemy import SQLAlchemyConnectionField
from session_schema import Session
from batch_schema import BatchOwner, Batch
from status_schema import Status
from event_schema import EventType, Event
from indicator_schema import IndicatorType, Indicator, IndicatorParameter, IndicatorResult
from data_source_schema import DataSourceType, DataSource
import graphene
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    batch = graphene.relay.Node.Field(Batch)
    batches = SQLAlchemyConnectionField(Batch)
    batch_owner = graphene.relay.Node.Field(BatchOwner)
    batch_owners = SQLAlchemyConnectionField(BatchOwner)
    data_source = graphene.relay.Node.Field(DataSource)
    data_sources = SQLAlchemyConnectionField(DataSource)
    data_source_type = graphene.relay.Node.Field(DataSourceType)
    data_source_types = SQLAlchemyConnectionField(DataSourceType)
    event_type = graphene.relay.Node.Field(EventType)
    event_types = SQLAlchemyConnectionField(EventType)
    event = graphene.relay.Node.Field(Event)
    events = SQLAlchemyConnectionField(Event)
    indicator = graphene.relay.Node.Field(Indicator)
    indicators = SQLAlchemyConnectionField(Indicator)
    indicator_parameter = graphene.relay.Node.Field(IndicatorParameter)
    indicator_parameters = SQLAlchemyConnectionField(IndicatorParameter)
    indicator_result = graphene.relay.Node.Field(IndicatorResult)
    indicator_results = SQLAlchemyConnectionField(IndicatorResult)
    indicator_type = graphene.relay.Node.Field(IndicatorType)
    indicator_types = SQLAlchemyConnectionField(IndicatorType)
    session = graphene.relay.Node.Field(Session)
    sessions = SQLAlchemyConnectionField(Session)
    status = graphene.relay.Node.Field(Status)
    statuses = SQLAlchemyConnectionField(Status)


schema = graphene.Schema(query=Query, auto_camelcase=False)
