from database import Database
import logging
import utils

utils.configLogger()
log = logging.getLogger(__name__)

class BatchOwner:
	"""Perform database operations on batch owners such as get, create, update, delete.
	Attributes:
		name: Batch owner name"""
	
	def __init__(self, name=None):
		self.name = name

	def get(self):
		"""Return a batch owner or a list of batch owners. If no batch owner name is provided return all batch owners."""
		log.info('Get batch owners')
		if not self.name: selectRecord = "select * from batch_owner order by batch_owner_id;"
		else: selectRecord = "select * from batch_owner where batch_owner='{}';".format(self.name)
		connection = Database()
		data = connection.executeQuery(selectRecord)
		return(data)

	def create(self):
		"""Create a batch owner"""
		log.info('Create batch owner')
		if not self.name: self.name = input('Enter batch owner name: ')
		insertRecord = "insert into batch_owner (batch_owner) values ('{}');".format(self.name)
		connection = Database()
		connection.executeQuery(insertRecord)
		return(True)

	def update(self, newName=None):
		"""Update a batch owner"""
		log.info('Update batch owner')
		if not self.name: self.name = input('Enter batch owner name: ')

		# Verify batch owner exist
		data = self.get()
		if len(data) == 0:
			log.info('Batch owner {} does not exist'.format(self.name))
			return(False)

		# If no new batch owner name is provided ask for new batch owner name
		if not newName: newName = input('Enter new batch owner name: ')
		updateRecord = "update batch_owner set batch_owner='{}', last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now') where batch_owner='{}';".format(newName, self.name)
		connection = Database()
		connection.executeQuery(updateRecord)
		self.name = newName
		return(True)

	def delete(self):
		"""Delete batch owner and all associated sessions and events"""
		log.info('Delete batch owner')
		if not self.name: self.name = input('Enter batch owner name: ')

		# Verify if batch owner is used by indicators
		# Tbd

		# Verify batch owner exist
		data = self.get()
		if len(data) == 0:
			log.info('Batch owner {} does not exist'.format(self.name))
			return(False)

		confirm = input('This will delete all events, sessions and batches for this batch owner. Are you sure (Y/n): ')
		if confirm == 'Y':
			connection = Database()

			log.info('Delete data in table: event')
			deleteEvent = """delete from event where event_id in (
			select event_id from event a
			inner join session b on a.session_id=b.session_id
			inner join batch c on b.batch_id=c.batch_id
			inner join batch_owner d on c.batch_owner_id=d.batch_owner_id
			where d.batch_owner='{}');""".format(self.name)
			connection.executeQuery(deleteEvent)

			log.info('Delete data in table: session')
			deleteSession = """delete from session where session_id in (
			select session_id from session a
			inner join batch b on a.batch_id=b.batch_id
			inner join batch_owner c on b.batch_owner_id=c.batch_owner_id
			where c.batch_owner='{}');""".format(self.name)
			connection.executeQuery(deleteSession)

			log.info('Delete data in table: batch')
			deleteBatch = """delete from batch where batch_id in (
			select batch_id from batch a
			inner join batch_owner b on a.batch_owner_id=b.batch_owner_id
			where b.batch_owner='{}');""".format(self.name)
			connection.executeQuery(deleteBatch)

			log.info('Delete data in table: batch_owner')
			deleteBatchOwner = "delete from batch_owner where batch_owner='{}';".format(self.name)
			connection.executeQuery(deleteBatchOwner)

			self.name=None
		return(True)