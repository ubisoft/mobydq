import logging
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Batch:
    """Batch class."""

    def __init__(self):
        pass

    @staticmethod
    def update_batch_status(batch_id, batch_status):
        """Update a batch status."""
        mutation = '''mutation{updateBatchById(input:{id:batch_id,batchPatch:{status:"batch_status"}}){batch{status}}}'''
        mutation = mutation.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('batch_status', str(batch_status))  # Use replace() instead of format() because of curly braces
        data = utils.execute_graphql_request(mutation)
        return data
