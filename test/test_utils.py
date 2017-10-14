"""Utility functions used by unit test scripts."""
from datetime import datetime
import inspect
import os
import sys
import time


# Modify python path to allow import module from parent folder
currentdirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdirectory = os.path.dirname(currentdirectory)
sys.path.insert(0, parentdirectory)


def testcasename(testcaselist):
    """Generate unique name for unit test case."""
    testcasename = 'Unit Test {}'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    for testcase in testcaselist:
        if testcasename in testcase['testcase']:
            time.sleep(1)
            testcasename = 'Unit Test {}'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    return testcasename
