from ast import literal_eval
from session import Session
import completeness  # Called dynamically with getattr
import freshness  # Called dynamically with getattr
import latency  # Called dynamically with getattr
import validity  # Called dynamically with getattr
import logging
import sys
import traceback
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Batch:
    """Batch class."""

    def __init__(self):
        pass

    def update_batch_status(self, batch_id: int, batch_status: str):
        """Update a batch status."""
        mutation = '''mutation{updateBatchById(input:{id:batch_id,batchPatch:{status:"batch_status"}}){batch{status}}}'''
        mutation = mutation.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('batch_status', str(batch_status))  # Use replace() instead of format() because of curly braces
        data = utils.execute_graphql_request(mutation)
        return data

    def execute(self, batch_id: int):
        log.info('Start execution of batch Id {batch_id}.'.format(batch_id=batch_id))

        # Get list of indicator sessions
        log.debug('Get list of indicator sessions.')
        query = '''query{allSessions(condition:{batchId:batch_id},orderBy:ID_ASC){
        nodes{id,batchId,indicatorId,indicatorByIndicatorId{name,indicatorTypeId,indicatorTypeByIndicatorTypeId{module,class,method},parametersByIndicatorId{
        nodes{parameterTypeId,value}}}}}}'''
        query = query.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
        response = utils.execute_graphql_request(query)

        if response['data']['allSessions']['nodes']:
            # Update batch status to running
            log.debug('Update batch status to Running.')
            self.update_batch_status(batch_id, 'Running')
            is_error = False  # Variable used to update batch status to Failed if one indicator fails

            # For each indicator session execute corresponding method
            for session in response['data']['allSessions']['nodes']:
                try:
                    module_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['module']
                    class_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['class']
                    method_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['method']
                    class_instance = getattr(sys.modules[module_name], class_name)()
                    getattr(class_instance, method_name)(session)

                except Exception:
                    is_error = True
                    error_message = traceback.format_exc()
                    log.error(error_message)

                    # Update session status
                    session_id = session['id']
                    Session.update_session_status(session_id, 'Failed')

                    # Get error context and send error e-mail
                    indicator_id = session['indicatorId']
                    indicator_name = session['indicatorByIndicatorId']['name']
                    for parameter in session['indicatorByIndicatorId']['parametersByIndicatorId']['nodes']:
                        if parameter['parameterTypeId'] == 3:  # Distribution list
                            distribution_list = literal_eval(parameter['value'])
                            utils.send_error(indicator_id, indicator_name, session_id, distribution_list, error_message)

            # Update batch status
            if is_error:
                log.debug('Update batch status to Failed.')
                self.update_batch_status(batch_id, 'Failed')
                log.warning('Batch Id {batch_id} completed with errors.'.format(batch_id=batch_id))
            else:
                log.debug('Update batch status to Succeeded.')
                self.update_batch_status(batch_id, 'Succeeded')
                log.info('Batch Id {batch_id} completed successfully.'.format(batch_id=batch_id))

        else:
            error_message = 'Batch Id {batch_id} does not exist or has no indicator session.'.format(batch_id=batch_id)
            log.error(error_message)
            raise Exception(error_message)
