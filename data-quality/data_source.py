from database import Database
import logging
import utils

utils.configLogger()
log = logging.getLogger(__name__)

class DataSource:
	"""Perform database operations on data sources such as get, create, update, delete.
	Attributes:
		name: Data source name.
		type: Data source type (Database, Api, File).
		connectionString: Connection string used to connect to the data source.
		login: Login used to connect to the data source.
		password: Password used to connect to the data source."""

	def __init__(self, name=None, type=None, connectionString=None, login=None, password=None):
		self.name = name
		self.type = type
		self.connectionString = connectionString
		self.login = login
		self.password = password

	def get(self):
		"""Return a data source or a list of data sources. If no data source name is provided return all data sources."""
		log.info('Get data sources')
		if not self.name: selectRecord = "select b.data_source_type, a.* from data_source a inner join data_source_type b on a.data_source_type_id= b.data_source_type_id order by data_source_id;"
		else: selectRecord = selectRecord = "select b.data_source_type, a.* from data_source a inner join data_source_type b on a.data_source_type_id= b.data_source_type_id where data_source='{}';".format(self.name)
		connection = Database()
		data = connection.executeQuery(selectRecord)
		return(data)

	def create(self, type=None):
		"""Create a data source"""
		log.info('Create data source')
		if not self.type: self.type = input('Enter data source type (Database, Api, File): ')
		
		# Verify data source type
		dataSourceType = DataSourceType(self.type)
		data = dataSourceType.get()
		if len(data) == 0:
			log.info('Data source type {} does not exist'.format(self.type))
			return(False)
		else: dataSourceTypeId = data[0]['data_source_type_id']

		if not self.name: self.name = input('Enter data source name: ')
		if not self.connectionString: self.connectionString = input('Enter connection string: ')
		if not self.login: self.login = input('Enter login: ')
		if not self.password: self.password = input('Enter password: ')
		insertRecord = "insert into data_source (data_source, data_source_type_id, connection_string, login, password) values ('{}','{}','{}','{}','{}');".format(self.name, dataSourceTypeId, self.connectionString, self.login, self.password)
		connection = Database()
		connection.executeQuery(insertRecord)
		return(True)

	def update(self):
		"""Update a data source"""
		log.info('Update data source')
		dataSourceType = input('Enter data source type (Database, Api, File): ')
		
		# Verify data source type id
		selectRecord = "select data_source_type_id from data_source_type where data_source_type='{}';".format(dataSourceType)
		connection = sqlite3.connect('data_quality.db')
		cursor = connection.cursor()
		cursor.execute(selectRecord)
		data = cursor.fetchall()
		if len(data) == 0:
			log.info('Data source type {} does not exist'.format(dataSourceType))
			return(False)
		else: dataSourceTypeId = data[0][0]

		dataSource = input('Enter existing data source name: ')
		newDataSource = input('Enter new data source name: ')
		connectionString = input('Enter connection string: ')
		login = input('Enter login: ')
		password = input('Enter password: ')

		# Connect to databas
		connection = sqlite3.connect('data_quality.db')
		cursor = connection.cursor()

		# Verify existing data source
		selectRecord = "select data_source from data_source where data_source='{}';".format(dataSource)
		cursor.execute(selectRecord)
		data = cursor.fetchall()
		if len(data) == 0:
			log.info('Data source {} does not exist'.format(dataSource))
			return(False)

		# Update data
		log.info('Update data in table: data_source')
		updateRecord = """update data_source set data_source='{}', data_source_type_id='{}', connection_string='{}',
		login='{}', password='{}', last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now') where data_source='{}';""".format(newDataSource, dataSourceTypeId, connectionString, login, password, dataSource)
		try: cursor.execute(updateRecord)
		except sqlite3.IntegrityError: log.info('Data source {} already exists'.format(newDataSource))

		# Save changes
		connection.commit()
		connection.close()
		return(True)

	def delete(self):
		"""Delete a data source"""
		log.info('Delete data source')
		dataSource = input('Enter data source name: ')

		# Verify if data source is used by indicators
		
		confirm = input('Are you sure (Y/n): ')
		if confirm == 'Y':
			# Connect to database
			connection = sqlite3.connect('data_quality.db')
			cursor = connection.cursor()

			# Delete data
			log.info('Delete data in table: data_source')
			deleteRecord = "delete from data_source where data_source='{}';".format(dataSource)
			cursor.execute(deleteRecord)

			# Close connection
			connection.commit()
			connection.close()
		return(True)

class DataSourceType:
	"""Perform database operations on data sources types such as get, create, update, delete.
	Attributes:
		name: Data source type name."""

	def __init__(self, name=None):
		self.name = name

	def get(self):
		"""Return a data source type or a list of data source types. If no data source type name is provided return all data source types."""
		log.info('Get data source type')
		if not self.name: selectRecord = "select * from data_source_type order by data_source_type_id;"
		else: selectRecord = "select * from data_source_type where data_source_type='{}';".format(self.name)
		connection = Database()
		data = connection.executeQuery(selectRecord)
		return(data)

	def create(self):
		"""Create a dats source type"""
		log.info('Create data source type')
		if not self.name: self.name = input('Enter data source type name: ')
		insertRecord = "insert into data_source_type (data_source_type) values ('{}');".format(self.name)
		connection = Database()
		connection.executeQuery(insertRecord)
		return(True)

	def update(self, newName=None):
		"""Update a data source type"""
		log.info('Update data source type')
		if not self.name: self.name = input('Enter data source type name: ')

		# Verify data source type exist
		data = self.get()
		if len(data) == 0:
			log.info('Data source type {} does not exist'.format(self.name))
			return(False)

		if not newName: newName = input('Enter new data source type name: ')
		updateRecord = "update data_source_type set data_source_type='{}', last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now') where data_source_type='{}';".format(newName, self.name)
		connection = Database()
		connection.executeQuery(updateRecord)
		self.name = newName
		return(True)

	def delete(self):
		"""Delete data source type"""
		log.info('Delete data source type')
		if not self.name: self.name = input('Enter data source type name: ')

		# Verify if data source type is used by data sources
		# Tbd

		# Verify data source type exist
		data = self.get()
		if len(data) == 0:
			log.info('Data source type {} does not exist'.format(self.name))
			return(False)

		confirm = input('This will delete the data source type. Are you sure (Y/n): ')
		if confirm == 'Y':
			log.info('Delete data in table: data_source_type')
			connection = Database()
			deleteDataSourceType = "delete from data_source_type where data_source_type='{}';".format(self.name)
			connection.executeQuery(deleteDataSourceType)

			self.name=None
		return(True)