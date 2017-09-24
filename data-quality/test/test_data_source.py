from data_source import DataSourceType
import logging
import unittest
import utils


log = logging.getLogger(__name__)


class TestDataSourceType(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        log.info('Start unit tests')

    def test_getWithoutName(self):
        data_source_type = DataSourceType()
        data_source_type.get()


if __name__ == '__main__':
    utils.configLogger()
    unittest.main()
