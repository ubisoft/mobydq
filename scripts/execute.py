import completeness
import freshness
import latency
import validity
import argparse
import logging
import sys
import utils


log = logging.getLogger(__name__)
logging.basicConfig(
    # filename='data_quality.log',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('batch_id', type=int, help='Id of the batch to be executed.')
    arguments = parser.parse_args()

    batch_id = arguments.batch_id
    log.info('Start execution of batch Id {batch_id}.'.format(batch_id=batch_id))

    # Update batch status to running
    log.debug('Update batch status to Running.')
    utils.update_batch_status(batch_id, 'Running')

    # Get list of indicator sessions
    log.debug('Get list of pending sessions.')
    query = '''query{allSessions(condition:{batchId:batch_id},orderBy:ID_ASC){
    nodes{id,batchId,indicatorByIndicatorId{id,name,indicatorTypeByIndicatorTypeId{id,module,class,method},parametersByIndicatorId{
    nodes{parameterTypeByParameterTypeId{name},value}}}}}}'''
    query = query.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
    data = utils.execute_graphql_request(query)

    # For each indicator session execute corresponding method
    for session in data['data']['allSessions']['nodes']:
        module_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['module']
        class_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['class']
        method_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['method']
        class_object = getattr(sys.modules[module_name], class_name)
        getattr(class_object, method_name)(data)

    # Update batch status to succeeded
    log.debug('Update batch status to Succeeded.')
    utils.update_batch_status(batch_id, 'Succeeded')
    log.info('Batch Id {batch_id} completed successfully.'.format(batch_id=batch_id))
