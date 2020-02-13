"""Manage class and methods for batches."""
import logging
import sys
import traceback
from ast import literal_eval
import completeness  # Called dynamically with getattr pylint: disable=W0611
import freshness  # Called dynamically with getattr pylint: disable=W0611
import latency  # Called dynamically with getattr pylint: disable=W0611
import validity  # Called dynamically with getattr pylint: disable=W0611
import utils
from session import Session

# Load logging configuration
log = logging.getLogger(__name__)


class Batch:
    """Batch class."""

    def update_batch_status(self, authorization: str, batch_id: int, batch_status: str):
        """Update a batch status."""

        query = 'mutation updateBatchStatus($id: Int!, $batchPatch: BatchPatch!){updateBatchById(input:{id: $id, batchPatch: $batchPatch}){batch{status}}}'
        variables = {'id': batch_id, 'batchPatch': {'status': batch_status}}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        return response

    def execute(self, authorization: str, batch_id: int):
        log.info('Start execution of batch Id %i.', batch_id)

        # Get list of indicator sessions
        log.debug('Get list of indicator sessions.')
        query = 'query getAllSessions($batchId: Int){allSessions(condition:{batchId: $batchId}, orderBy:ID_ASC){nodes{id, batchId, indicatorId, userGroupId, indicatorByIndicatorId{name, indicatorTypeId, indicatorTypeByIndicatorTypeId{module, class, method}, parametersByIndicatorId{nodes{parameterTypeId, value}}}}}}'
        variables = {'batchId': batch_id}
        payload = {'query': query, 'variables': variables}
        response = utils.execute_graphql_request(authorization, payload)

        if response['data']['allSessions']['nodes']:
            # Update batch status to running
            log.debug('Update batch status to Running.')
            self.update_batch_status(authorization, batch_id, 'Running')
            is_error = False  # Variable used to update batch status to Failed if one indicator fails

            # Loop over each indicator session
            for session in response['data']['allSessions']['nodes']:
                try:
                    # Recreate custom log handler to add session Id to context
                    root_log = logging.getLogger()
                    custom_handler = root_log.handlers[1]
                    root_log.removeHandler(custom_handler)
                    root_log.addHandler(utils.CustomLogHandler(authorization, batch_id=batch_id, session_id=session['id']))

                    # For each session execute indicator type method
                    module_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['module']
                    class_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['class']
                    method_name = session['indicatorByIndicatorId']['indicatorTypeByIndicatorTypeId']['method']
                    class_instance = getattr(sys.modules[module_name], class_name)()
                    getattr(class_instance, method_name)(authorization, session)

                except Exception: # pylint: disable=broad-except
                    is_error = True
                    error_message = traceback.format_exc()
                    log.error(error_message)

                    # Update session status
                    session_id = session['id']
                    Session().update_session_status(authorization, session_id, 'Failed')

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
                self.update_batch_status(authorization, batch_id, 'Failed')
                log.warning('Batch Id %i completed with errors.', batch_id)
            else:
                log.debug('Update batch status to Success.')
                self.update_batch_status(authorization, batch_id, 'Success')
                log.info('Batch Id %i completed successfully.', batch_id)

        else:
            error_message = f'Batch Id {batch_id} does not exist or has no indicator session.'
            log.error(error_message)
            raise Exception(error_message)
