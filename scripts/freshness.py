from datetime import datetime
from indicator import Indicator
import logging
import pandas

# Load logging configuration
log = logging.getLogger(__name__)


class Freshness(Indicator):
    """Class used to compute indicators of type freshness."""

    def __init__(self):
        pass

    def execute(self, data):
        print('init freshness')

    def evaluate_freshness(self, data_sets, parameters):
        """Compute specificities of freshness indicator."""
        result_data_frame = data_sets['Target data frame']
        result_data_frame['current_timestamp'] = datetime.utcnow()

        # Prepare variables
        alert_operator = parameters[1]  # Alert operator
        alert_threshold = parameters[2]  # Alert threshold
        measure_list = parameters[3]  # Measure

        # Compute delta in minutes and delta description between source and target measures
        for measure in measure_list:
            source_column = 'current_timestamp'
            target_column = measure
            delta_column = measure + '_delta_minutes'
            delta_description_column = measure + '_delta_description'

            # Enforce measure to datetime data type
            result_data_frame[source_column] = pandas.to_datetime(result_data_frame[source_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
            result_data_frame[target_column] = pandas.to_datetime(result_data_frame[target_column], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')

            # Compute delta and delta description
            delta_seconds = (result_data_frame[source_column] - result_data_frame[target_column]).dt.total_seconds()
            result_data_frame[delta_column] = round(delta_seconds/60).astype(int)
            result_data_frame[delta_description_column] = pandas.to_timedelta(delta_seconds, unit='s')

        # For each record and measure in data frame, test if alert must be sent and update alert column
        result_data_frame['Alert'] = False
        for measure in measure_list:
            for row_num in result_data_frame.index:
                measure_value = result_data_frame.loc[row_num, measure + '_delta_minutes']
                measure_value = abs(measure_value)*100
                if self.is_alert(measure_value, alert_operator, alert_threshold):
                    result_data_frame.loc[row_num, 'Alert'] = True
        return result_data_frame
