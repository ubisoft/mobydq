from sqlalchemy import event
from sqlalchemy.engine import Engine


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(db_api_connection, connection_record):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = db_api_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
