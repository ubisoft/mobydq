#!/usr/bin/env python
"""Utility functions used by unit test scripts."""
from datetime import datetime
import inspect
import os
import sys
import time


# Modify python path to allow import module from parent folder
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_directory = os.path.dirname(current_directory)
sys.path.insert(0, parent_directory)


def get_test_case_name(test_case_list):
    """Generate unique name for unit test case."""
    test_case_name = 'unit_test_{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for test_case in test_case_list:
        if test_case_name in test_case['test_case']:
            time.sleep(1)
            test_case_name = 'unit_test_{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return test_case_name
