from graphene_sqlalchemy import SQLAlchemyConnectionField
from schema_data_source import SchemaDataSource, SchemaDataSourceType
from schema_session import SchemaSession
from schema_batch import SchemaBatch, SchemaBatchOwner
from schema_event import SchemaEvent, SchemaEventType
from schema_indicator import SchemaIndicator, SchemaIndicatorParameter, SchemaIndicatorParameterType, SchemaIndicatorResult, SchemaIndicatorType
from schema_status import SchemaStatus
import graphene
import logging
import mutation_batch
import mutation_data_source
import mutation_event
import mutation_indicator
import mutation_session
import mutation_status

# Load logging configuration
log = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    """List of objects which can be queried from this API."""

    node = graphene.relay.Node.Field()

    # Batch queries
    batch = graphene.relay.Node.Field(SchemaBatch)
    batches = SQLAlchemyConnectionField(SchemaBatch)
    batchOwner = graphene.relay.Node.Field(SchemaBatchOwner)
    batchOwners = SQLAlchemyConnectionField(SchemaBatchOwner)

    # Data source queries
    dataSource = graphene.relay.Node.Field(SchemaDataSource)
    dataSources = SQLAlchemyConnectionField(SchemaDataSource)
    dataSourceType = graphene.relay.Node.Field(SchemaDataSourceType)
    dataSourceTypes = SQLAlchemyConnectionField(SchemaDataSourceType)

    # Event queries
    event = graphene.relay.Node.Field(SchemaEvent)
    events = SQLAlchemyConnectionField(SchemaEvent)
    eventType = graphene.relay.Node.Field(SchemaEventType)
    eventTypes = SQLAlchemyConnectionField(SchemaEventType)

    # Indicator queries
    indicator = graphene.relay.Node.Field(SchemaIndicator)
    indicators = SQLAlchemyConnectionField(SchemaIndicator)
    indicatorParameter = graphene.relay.Node.Field(SchemaIndicatorParameter)
    indicatorParameters = SQLAlchemyConnectionField(SchemaIndicatorParameter)
    indicatorParameterType = graphene.relay.Node.Field(SchemaIndicatorParameterType)
    indicatorParameterTypes = SQLAlchemyConnectionField(SchemaIndicatorParameterType)
    indicatorResult = graphene.relay.Node.Field(SchemaIndicatorResult)
    indicatorResults = SQLAlchemyConnectionField(SchemaIndicatorResult)
    indicatorType = graphene.relay.Node.Field(SchemaIndicatorType)
    indicatorTypes = SQLAlchemyConnectionField(SchemaIndicatorType)

    # Session queries
    session = graphene.relay.Node.Field(SchemaSession)
    sessions = SQLAlchemyConnectionField(SchemaSession)

    # Status queries
    status = graphene.relay.Node.Field(SchemaStatus)
    statuses = SQLAlchemyConnectionField(SchemaStatus)


class Mutation(graphene.ObjectType):
    """List of mutations which can be performed from this API."""

    # Create batch mutations
    createBatch = mutation_batch.CreateBatch.Field()
    createBatchOwner = mutation_batch.CreateBatchOwner.Field()

    # Create data source mutations
    createDataSource = mutation_data_source.CreateDataSource.Field()
    createDataSourceType = mutation_data_source.CreateDataSourceType.Field()

    # Create event mutations
    createEvent = mutation_event.CreateEvent.Field()
    createEventType = mutation_event.CreateEventType.Field()

    # Create indicator mutations
    createIndicator = mutation_indicator.CreateIndicator.Field()
    createIndicatorParameter = mutation_indicator.CreateIndicatorParameter.Field()
    createIndicatorParameterType = mutation_indicator.CreateIndicatorParameterType.Field()
    createIndicatorResult = mutation_indicator.CreateIndicatorResult.Field()
    createIndicatorType = mutation_indicator.CreateIndicatorType.Field()

    # Create session mutations
    createSession = mutation_session.CreateSession.Field()

    # Create status mutations
    createStatus = mutation_status.CreateStatus.Field()

    # Execute batch mutation
    execute_batch = mutation_batch.ExecuteBatch.Field()

    # Update batch mutations
    update_batch = mutation_batch.UpdateBatch.Field()
    update_batch_owner = mutation_batch.UpdateBatchOwner.Field()

    # Update data source mutations
    update_data_source = mutation_data_source.UpdateDataSource.Field()
    update_data_source_type = mutation_data_source.UpdateDataSourceType.Field()

    # Update event mutations
    update_event = mutation_event.UpdateEvent.Field()
    update_event_type = mutation_event.UpdateEventType.Field()

    # Update indicator mutations
    updateIndicator = mutation_indicator.UpdateIndicator.Field()
    updateIndicatorParameter = mutation_indicator.UpdateIndicatorParameter.Field()
    updateIndicatorParameterType = mutation_indicator.UpdateIndicatorParameterType.Field()
    updateIndicatorResult = mutation_indicator.UpdateIndicatorResult.Field()
    updateIndicatorType = mutation_indicator.UpdateIndicatorType.Field()

    # Update session mutations
    update_session = mutation_session.UpdateSession.Field()

    # Update status mutations
    update_status = mutation_status.UpdateStatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
