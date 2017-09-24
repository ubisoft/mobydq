import data_source
import unittest

utils.configLogger()
log = logging.getLogger(__name__)

class TestDataSourceType(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		log.info('Start unit tests')

	def test_getWithoutName(self):
		DataSourceType = DataSourceType()
		result = DataSourceType.get()


if __name__ == '__main__':
	unittest.main()