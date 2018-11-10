"""Manage class and methods for data anomaly indicators."""
import logging
from indicator import Indicator

# Load logging configuration
log = logging.getLogger(__name__)


class AnomalyDetection(Indicator):
    """Class used to compute indicators of type anomaly detection."""

    def execute(self, session: dict):
        pass
