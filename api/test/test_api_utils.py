"""Utility functions used by API unit test scripts."""
import inspect
import os
import sys


# Modify python path to allow import module from grand parent folder
currentdirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdirectory = os.path.dirname(currentdirectory)
grandparentdirectory = os.path.dirname(parentdirectory)
sys.path.insert(0, grandparentdirectory)
