import logging
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Session:
    """Session class."""

    def __init__(self):
        pass

    @staticmethod
    def update_session_status(session_id, session_status):
        """Update a session status."""
        mutation = '''mutation{updateSessionById(input:{id:session_id,sessionPatch:{status:"session_status"}}){session{status}}}'''
        mutation = mutation.replace('session_id', str(session_id))  # Use replace() instead of format() because of curly braces
        mutation = mutation.replace('session_status', str(session_status))  # Use replace() instead of format() because of curly braces
        data = utils.execute_graphql_request(mutation)
        return data
