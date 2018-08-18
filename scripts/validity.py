from indicator import Indicator
import logging

# Load logging configuration
log = logging.getLogger(__name__)


class Validity(Indicator):
    """Class used to compute indicators of type validity."""

    def __init__(self):
        pass

    def execute(self, data):
        print('init validity')

    def evaluate_validity(self, data_sets, parameters):
        """Compute specificities of validity indicator."""
        # No tranformation needed for this data frame
        result_data_frame = data_sets['Target data frame']

        # Prepare variables
        alert_operator = parameters[1]  # Alert operator
        alert_threshold = parameters[2]  # Alert threshold
        measure_list = parameters[3]  # Measure

        # Formatting data to improve readability
        for measure in measure_list:
            result_data_frame[measure] = round(result_data_frame[measure], 2).astype(float)

        # For each record and measure in data frame, test if alert must be sent and update alert column
        result_data_frame['Alert'] = False
        for measure in measure_list:
            for row_num in result_data_frame.index:
                measure_value = result_data_frame.loc[row_num, measure]
                if self.is_alert(measure_value, alert_operator, alert_threshold):
                    result_data_frame.loc[row_num, 'Alert'] = True
        return result_data_frame
