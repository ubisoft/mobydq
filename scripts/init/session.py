"""Manage class and methods for sessions."""
import logging
import utils

# Load logging configuration
log = logging.getLogger(__name__)


def update_session_status(session_id: int, session_status: str):
    """Update a session status."""
    mutation = '''mutation{updateSessionById(input:{id:session_id,sessionPatch:{status:"session_status"}}){session{status}}}'''
    mutation = mutation.replace('session_id', str(
        session_id))  # Use replace() instead of format() because of curly braces
    # Use replace() instead of format() because of curly braces
    mutation = mutation.replace('session_status', str(session_status))
    data = utils.execute_graphql_request(mutation)
    return data
