"""Utility functions used by unit test scripts."""
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time


def testcasename(testcaselist):
    """Generate unique name for unit test case."""
    testcasename = 'Unit Test {}'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    if testcasename in testcaselist:
        time.sleep(1)
        testcasename = 'Unit Test {}'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    return testcasename


@event.listens_for(Engine, 'connect')
def setsqlitepragma(dbapiconnection, connectionrecord):
    """Activate sqlite pragma to enforce foreign keys integrity, in particular for cascade delete."""
    cursor = dbapiconnection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
