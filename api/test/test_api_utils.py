"""Utility functions used by API unit test scripts."""
import inspect
import os
import sys


# Modify python path to allow import module from grand parent folder
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_directory = os.path.dirname(current_directory)
grand_parent_directory = os.path.dirname(parent_directory)
sys.path.insert(0, grand_parent_directory)
