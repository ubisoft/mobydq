import argparse
import ast
import logging
import sqlite3
import utils

utils.configLogger()
log = logging.getLogger(__name__)

class Database:
	"""Perform database operations on dataquality.db."""

	def __enter__(self):
		self.connection = sqlite3.connect('data_quality.db')
		self.connection.row_factory = utils.dictionary # Converts cursor result to dictionary
		self.cursor = self.connection.cursor()
		return self

	def __exit__(self, ext_type, exc_value, traceback):
		self.connection.commit()
		self.connection.close()

	def executeQuery(self, query):
		"""Execute an SQL query on data_quality.db."""
		cursorResult = self.cursor.execute(query)
		dictionary = cursorResult.fetchall()
		return(dictionary)

	def setUp(self):
		"""Create tables and populate them with default list of values."""

		log.info('Create table if not exists: data_source_type')
		# Data source type
		self.cursor.execute('''create table if not exists data_source_type(
			data_source_type_id integer primary key autoincrement,
			data_source_type text unique,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
			''')

		# Data source
		log.info('Create table if not exists: data_source')
		self.cursor.execute('''create table if not exists data_source(
			data_source_id integer primary key autoincrement,
			data_source text unique,
			data_source_type_id integer,
			connection_string text,
			login text,
			password text,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_data_source_type foreign key (data_source_type_id) references data_source_type(data_source_type_id))
			''')

		# Status
		log.info('Create table if not exists: status')
		self.cursor.execute('''create table if not exists status(
			status_id integer primary key autoincrement,
			status text unique,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
			''')

		# Batch owner
		log.info('Create table if not exists: batch_owner')
		self.cursor.execute('''create table if not exists batch_owner(
			batch_owner_id integer primary key autoincrement,
			batch_owner text unique,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
			''')

		# Batch
		log.info('Create table if not exists: batch')
		self.cursor.execute('''create table if not exists batch(
			batch_id integer primary key autoincrement,
			status_id integer,
			batch_owner_id integer,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_status foreign key (status_id) references status(status_id),
			constraint fk_batch_owner foreign key (batch_owner_id) references batch_owner(batch_owner_id))
			''')

		# Indicator type
		log.info('Create table if not exists: indicator_type')
		self.cursor.execute('''create table if not exists indicator_type(
			indicator_type_id integer primary key autoincrement,
			indicator_type text unique,
			module text,
			function text,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
			''')

		# Indicator
		log.info('Create table if not exists: indicator')
		self.cursor.execute('''create table if not exists indicator(
			indicator_id integer primary key autoincrement,
			indicator text unique,
			indicator_description text,
			indicator_type_id integer,
			batch_owner_id integer,
			execution_order integer,
			alert_operator text,
			alert_threshold real,
			alert_distribution_list text,
			flag_active integer,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_indicator_type foreign key (indicator_type_id) references indicator_type(indicator_type_id),
			constraint fk_batch_owner foreign key (batch_owner_id) references batch_owner(batch_owner_id))
			''')

		# Indicator parameter
		log.info('Create table if not exists: indicator_parameter')
		self.cursor.execute('''create table if not exists indicator_parameter(
			indicator_parameter_id integer primary key autoincrement,
			indicator_parameter text,
			indicator_parameter_value blob,
			indicator_id integer,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_indicator foreign key (indicator_id) references indicator(indicator_id))
			''')

		# Indicator result
		log.info('Create table if not exists: indicator_result')
		self.cursor.execute('''create table if not exists indicator_result(
			indicator_result_id integer primary key autoincrement,
			indicator_id integer,
			session_id integer,
			alert_operator text,
			alert_threshold real,
			nb_records integer,
			nb_records_alert integer,
			nb_records_no_alert integer,
			avg_result real,
			avg_result_alert real,
			avg_result_no_alert real,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_indicator foreign key (indicator_id) references indicator(indicator_id),
			constraint fk_session foreign key (session_id) references session(session_id))
			''')

		# Session
		log.info('Create table if not exists: session')
		self.cursor.execute('''create table if not exists session(
			session_id integer primary key autoincrement,
			status_id integer,
			batch_id integer,
			indicator_id integer,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_status foreign key (status_id) references status(status_id),
			constraint fk_batch_owner foreign key (batch_id) references batch(batch_id),
			constraint fk_indicator foreign key (indicator_id) references indicator(indicator_id))
			''')

		# Event type
		log.info('Create table if not exists: event_type')
		self.cursor.execute('''create table if not exists event_type(
			event_type_id integer primary key autoincrement,
			event_type text unique,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
			''')

		# Event
		log.info('Create table if not exists: event')
		self.cursor.execute('''create table if not exists event(
			event_id integer primary key autoincrement,
			event_type_id integer,
			event_content blob,
			session_id integer,
			created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
			constraint fk_event_type foreign key (event_type_id) references event_type(event_type_id),
			constraint fk_session foreign key (session_id) references session(session_id))
			''')

		log.info('Insert list of values into database')

		# Insert data
		with open('data_quality.dat','r') as dataFile:
			dataDictionary = ast.literal_eval(dataFile.read())
			for table in dataDictionary['list_of_values']:
				log.info('Insert data in table: {}'.format(table['table']))
				insertTable = utils.updateQuery("insert into {{table}} ({{columns}})", table)
				for record in table['records']:
					insertRecord = utils.updateQuery(insertTable + " values ({{values}});", record)
					try: self.cursor.execute(insertRecord)
					except sqlite3.IntegrityError: log.info('Table {}, value already exists: {}'.format(table['table'], record['values']))

		return(True)

if __name__ == '__main__':
	Database = Database()
	Database.setUp()