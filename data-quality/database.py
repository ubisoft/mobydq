import argparse
import sys
import sqlite3
import ast
import utils

# Create database and tables
def initDatabase():
	print('Initialize database')

	# Create database
	print('Create database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Create tables
	print('Create table if not exists: data_source_type')
	# Data source type
	cursor.execute('''create table if not exists data_source_type(
		data_source_type_id integer primary key autoincrement,
		data_source_type text unique,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
		''')

	# Data source
	print('Create table if not exists: data_source')
	cursor.execute('''create table if not exists data_source(
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
	print('Create table if not exists: status')
	cursor.execute('''create table if not exists status(
		status_id integer primary key autoincrement,
		status text unique,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
		''')

	# Batch owner
	print('Create table if not exists: batch_owner')
	cursor.execute('''create table if not exists batch_owner(
		batch_owner_id integer primary key autoincrement,
		batch_owner text unique,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
		''')

	# Batch
	print('Create table if not exists: batch')
	cursor.execute('''create table if not exists batch(
		batch_id integer primary key autoincrement,
		status_id integer,
		batch_owner_id integer,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		constraint fk_status foreign key (status_id) references status(status_id),
		constraint fk_batch_owner foreign key (batch_owner_id) references batch_owner(batch_owner_id))
		''')

	# Indicator type
	print('Create table if not exists: indicator_type')
	cursor.execute('''create table if not exists indicator_type(
		indicator_type_id integer primary key autoincrement,
		indicator_type text unique,
		module text,
		function text,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
		''')

	# Indicator
	print('Create table if not exists: indicator')
	cursor.execute('''create table if not exists indicator(
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
	print('Create table if not exists: indicator_parameter')
	cursor.execute('''create table if not exists indicator_parameter(
		indicator_parameter_id integer primary key autoincrement,
		indicator_parameter text,
		indicator_parameter_value blob,
		indicator_id integer,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		constraint fk_indicator foreign key (indicator_id) references indicator(indicator_id))
		''')

	# Indicator result
	print('Create table if not exists: indicator_result')
	cursor.execute('''create table if not exists indicator_result(
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
	print('Create table if not exists: session')
	cursor.execute('''create table if not exists session(
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
	print('Create table if not exists: event_type')
	cursor.execute('''create table if not exists event_type(
		event_type_id integer primary key autoincrement,
		event_type text unique,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		last_updated_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')))
		''')

	# Event
	print('Create table if not exists: event')
	cursor.execute('''create table if not exists event(
		event_id integer primary key autoincrement,
		event_type_id integer,
		event_content blob,
		session_id integer,
		created_date datetime default(strftime('%Y-%m-%d %H:%M:%f', 'now')),
		constraint fk_event_type foreign key (event_type_id) references event_type(event_type_id),
		constraint fk_session foreign key (session_id) references session(session_id))
		''')

	# Save changes
	connection.commit()
	connection.close()
	return(True)

# Insert default list of values into database
def postListOfValues():
	print('Insert list of values into database')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Insert data
	dataFile = open('data_quality.dat','r')
	dataDictionary = ast.literal_eval(dataFile.read())
	for table in dataDictionary['list_of_values']:
		print('Insert data in table: {}'.format(table['table']))
		insertTable = utils.updateQuery("insert into {{table}} ({{columns}})", table)
		for record in table['records']:
			insertRecord = utils.updateQuery(insertTable + " values ({{values}});", record)
			try: cursor.execute(insertRecord)
			except sqlite3.IntegrityError: print('Table {}, value already exists: {}'.format(table['table'], record['values']))

	# Save changes
	connection.commit()
	connection.close()
	return(True)

# Create a batch owner
def postBatchOwner():
	print('Create a batch owner')
	batchOwner = input('Enter batch owner name: ')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Insert data
	print('Insert data in table: batch_owner')
	insertRecord = "insert into batch_owner (batch_owner) values ('{}');".format(batchOwner)
	try: cursor.execute(insertRecord)
	except sqlite3.IntegrityError: print('Batch owner {} already exists'.format(batchOwner))

	# Save changes
	connection.commit()
	connection.close()
	return(True)

# Update a batch owner
def putBatchOwner():
	print('Update a batch owner')
	batchOwner = input('Enter existing batch owner name: ')
	newBatchOwner = input('Enter new batch owner name: ')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Verify existing batch owner
	selectRecord = "select batch_owner from batch_owner where batch_owner='{}';".format(batchOwner)
	cursor.execute(selectRecord)
	data = cursor.fetchall()
	if len(data) == 0:
		print('Batch owner {} does not exist'.format(batchOwner))
		return(False)

	# Update data
	print('Update data in table: batch_owner')
	updateRecord = "update batch_owner set batch_owner='{}', last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now') where batch_owner='{}';".format(newBatchOwner, batchOwner)
	cursor.execute(updateRecord)
	try: cursor.execute(updateRecord)
	except sqlite3.IntegrityError: print('Batch owner {} already exists'.format(newBatchOwner))

	# Save changes
	connection.commit()
	connection.close()
	return(True)

# Get batch owners
def getBatchOwner():
	print('Get batch owners')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Select data
	print('(batch_owner_id, batch_owner, created_date, last_updated_date)')
	selectRecord = "select * from batch_owner order by batch_owner_id;"
	cursor.execute(selectRecord)
	for record in cursor:
		print(record)

	# Close connection
	connection.close()
	return(True)

# Create a data source
def postDataSource():
	print('Create a data source')
	dataSource = input('Enter data source name: ')
	dataSourceType = input('Enter data source type (Database, Api, File): ')
	connectionString = input('Enter connection string: ')
	login = input('Enter login: ')
	password = input('Enter password: ')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Get data source type id
	selectRecord = "select data_source_type_id from data_source_type where data_source_type='{}';".format(dataSourceType)
	cursor.execute(selectRecord)
	data = cursor.fetchall()
	if len(data) == 0:
		print('Data source type {} does not exist'.format(dataSourceType))
		return(False)
	else: dataSourceTypeId = data[0][0]

	# Insert data
	print('Insert data in table: data_source')
	insertRecord = "insert into data_source (data_source, data_source_type_id, connection_string, login, password) values ('{}','{}','{}','{}','{}');".format(dataSource, dataSourceTypeId, connectionString, login, password)
	try: cursor.execute(insertRecord)
	except sqlite3.IntegrityError: print('Data source {} already exists'.format(dataSource))

	# Save changes
	connection.commit()
	connection.close()
	return(True)

# Update a data source
def putDataSource():
	return(True)

# Get data sources
def getDataSource():
	print('Get data sources')

	# Connect to database
	print('Connect to database data_quality.db')
	connection = sqlite3.connect('data_quality.db')
	cursor = connection.cursor()

	# Select data
	print('(data_source_id, data_source, data_source_type, connection_string, created_date, last_updated_date)')
	selectRecord = """select a.data_source_id, a.data_source, b.data_source_type, a.connection_string, a.created_date, a.last_updated_date
	from data_source a inner join data_source_type b on a.data_source_type_id= b.data_source_type_id order by data_source_id;"""
	cursor.execute(selectRecord)
	for record in cursor:
		print(record)

	# Close connection
	connection.close()
	return(True)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='function', type=str, help='Enter the name of the function you wish to exectue', choices=['initDatabase','postListOfValues','postBatchOwner','putBatchOwner','getBatchOwner', 'postDataSource','putDataSource','getDataSource'])
	arguments = parser.parse_args()

	# Execute module
	if not arguments.function:
		getattr(sys.modules[__name__], 'initDatabase')()
		getattr(sys.modules[__name__], 'postListOfValues')()
	else:
		getattr(sys.modules[__name__], arguments.function)()
