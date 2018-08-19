from ast import literal_eval
import logging
import os
import utils

# Load logging configuration
log = logging.getLogger(__name__)


class Indicator:
    """Base class used to compute indicators, regardless of their type."""

    def __init__(self):
        pass
