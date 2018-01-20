from graphene_sqlalchemy import SQLAlchemyConnectionField
from session_schema import Session
from batch_schema import BatchOwner, Batch
from status_schema import Status
from event_schema import EventType, Event
from indicator_schema import IndicatorType, Indicator, IndicatorParameter, IndicatorResult
from data_source_schema import DataSourceType, DataSource
import graphene


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    batch_owner = graphene.relay.Node.Field(BatchOwner)
    all_batch_owners = SQLAlchemyConnectionField(BatchOwner)

    indicator = graphene.relay.Node.Field(Indicator)
    all_indicators = SQLAlchemyConnectionField(Indicator)


schema = graphene.Schema(query=Query)
