from graphene_sqlalchemy import SQLAlchemyConnectionField
import graphene
import logging
import mutation_batch
import mutation_data_source
import schema_batch
import schema_data_source
import schema_event
import schema_indicator
import schema_session
import schema_status


# Load logging configuration
log = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    """Query endpoint for GraphQL API."""

    node = graphene.relay.Node.Field()

    # Batch queries
    batch = graphene.relay.Node.Field(schema_batch.Batch)
    batches = SQLAlchemyConnectionField(schema_batch.Batch)
    batch_owner = graphene.relay.Node.Field(schema_batch.BatchOwner)
    batch_owners = SQLAlchemyConnectionField(schema_batch.BatchOwner)

    # Data source queries
    data_source = graphene.relay.Node.Field(schema_data_source.DataSource)
    data_sources = SQLAlchemyConnectionField(schema_data_source.DataSource)
    data_source_type = graphene.relay.Node.Field(schema_data_source.DataSourceType)
    data_source_types = SQLAlchemyConnectionField(schema_data_source.DataSourceType)

    # Event queries
    event = graphene.relay.Node.Field(schema_event.Event)
    events = SQLAlchemyConnectionField(schema_event.Event)
    event_type = graphene.relay.Node.Field(schema_event.EventType)
    event_types = SQLAlchemyConnectionField(schema_event.EventType)

    # Indicator queries
    indicator = graphene.relay.Node.Field(schema_indicator.Indicator)
    indicators = SQLAlchemyConnectionField(schema_indicator.Indicator)
    indicator_parameter = graphene.relay.Node.Field(schema_indicator.IndicatorParameter)
    indicator_parameters = SQLAlchemyConnectionField(schema_indicator.IndicatorParameter)
    indicator_result = graphene.relay.Node.Field(schema_indicator.IndicatorResult)
    indicator_results = SQLAlchemyConnectionField(schema_indicator.IndicatorResult)
    indicator_type = graphene.relay.Node.Field(schema_indicator.IndicatorType)
    indicator_types = SQLAlchemyConnectionField(schema_indicator.IndicatorType)

    # Session queries
    session = graphene.relay.Node.Field(schema_session.Session)
    sessions = SQLAlchemyConnectionField(schema_session.Session)

    # Status queries
    status = graphene.relay.Node.Field(schema_status.Status)
    statuses = SQLAlchemyConnectionField(schema_status.Status)


class Mutation(graphene.ObjectType):
    """Mutation endpoint for GraphQL API."""

    # Batch mutations
    create_batch = mutation_batch.CreateBatch.Field()
    create_batch_owner = mutation_batch.CreateBatchOwner.Field()
    execute_batch = mutation_batch.ExecuteBatch.Field()
    update_batch = mutation_batch.UpdateBatch.Field()
    update_batch_owner = mutation_batch.UpdateBatchOwner.Field()

    # Data source mutations
    create_data_source = mutation_data_source.CreateDataSource.Field()
    create_data_source_type = mutation_data_source.CreateDataSourceType.Field()
    update_data_source = mutation_data_source.UpdateDataSource.Field()
    update_data_source_type = mutation_data_source.UpdateDataSourceType.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
