from database import Database
import logging
import utils

utils.configLogger()
log = logging.getLogger(__name__)


class DataSourceType:
    """Perform database operations on data sources types such as get, create, update, delete.
    Attributes:

    name: Data source type name."""

    def __init__(self, name=None):
        self.name = name

    def get(self):
        """Return a data source type or a list of data source types."""
        log.info('Get data source type')

        # If no data source type name is provided return all data source types.
        if not self.name:
            selectRecord = "select * from data_source_type order by data_source_type_id;"
        else:
            selectRecord = "select * from data_source_type where data_source_type='{}';".format(self.name)

        # Execute query.
        with Database() as connection:
            data = connection.executeQuery(selectRecord)

        return(data)

    def create(self):
        """Create a dats source type."""
        log.info('Create data source type')

        # If no data source type name is provided ask for it.
        if not self.name:
            self.name = input('Enter data source type name: ')

        # Execute query.
        insertRecord = "insert into data_source_type (data_source_type) values ('{}');".format(self.name)
        with Database() as connection:
            connection.executeQuery(insertRecord)

        return(True)

    def update(self, newName=None):
        """Update a data source type."""
        log.info('Update data source type')

        # If no data source type name is provided ask for it.
        if not self.name:
            self.name = input('Enter data source type name: ')

        # Verify data source type exist.
        data = self.get()
        if len(data) == 0:
            log.info('Data source type {} does not exist'.format(self.name))
            self.name = None
            return(False)

        # If no new data source type name is provided ask for it.
        if not newName:
            newName = input('Enter new data source type name: ')

        # Execute query.
        updateRecord = """update data_source_type set data_source_type='{}',
                       last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now') where data_source_type='{}';""".format(
                            newName, self.name
                       )
        with Database() as connection:
            connection.executeQuery(updateRecord)

        # Update data source type name attribute to new name.
        self.name = newName
        return(True)

    def delete(self):
        """Delete data source type."""
        log.info('Delete data source type')

        # If no data source type name is provided ask for it.
        if not self.name:
            self.name = input('Enter data source type name: ')

        # Verify data source type exist.
        data = self.get()
        if len(data) == 0:
            log.info('Data source type {} does not exist'.format(self.name))
            self.name = None
            return(False)

        # Verify data source type is not used by data source.
        selectRecord = """select data_source from data_source where data_source_type_id='{}';""".format(
            data[0]['data_source_type_id']
        )
        with Database() as connection:
            dataSource = connection.executeQuery(selectRecord)
            if len(dataSource) != 0:
                log.info('Data source type {} is used by the following data sources and cannot be deleted: {}'.format(
                    self.name, dataSource
                ))
                return(False)

        # Confirm and execute query.
        if input('This will delete the data source type. Are you sure (Y/n): ') == 'Y':
            deleteDataSourceType = "delete from data_source_type where data_source_type_id='{}';".format(
                data[0]['data_source_type_id']
            )
            with Database() as connection:
                connection.executeQuery(deleteDataSourceType)

        # Update data source type name attribute to none since it got deleted.
        self.name = None
        return(True)


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
        """Return a data source or a list of data sources."""
        log.info('Get data sources')

        # If no data source name is provided return all data sources.
        if not self.name:
            selectRecord = """
                select b.data_source_type, a.*
                from data_source a
                inner join data_source_type b
                on a.data_source_type_id= b.data_source_type_id order by data_source_id;
            """
        else:
            selectRecord = """
                select b.data_source_type, a.*
                from data_source a
                inner join data_source_type b on a.data_source_type_id = b.data_source_type_id
                where data_source='{}';""".format(self.name)

        # Execute query.
        with Database() as connection:
            data = connection.executeQuery(selectRecord)

        return(data)

    def create(self):
        """Create a data source."""
        log.info('Create data source')

        # If no data source type name is provided ask for it.
        if not self.type:
            self.type = input('Enter data source type (Database, Api, File): ')

        # Verify data source type exist.
        dataSourceType = DataSourceType(self.type)
        data = dataSourceType.get()
        if len(data) != 0:
            dataSourceTypeId = data[0]['data_source_type_id']
        else:
            log.info('Data source type {} does not exist'.format(self.type))
            self.type = None
            return(False)

        # If other attributes are not provided ask for them.
        if not self.name:
            self.name = input('Enter data source name: ')

        if not self.connectionString:
            self.connectionString = input('Enter connection string: ')

        if not self.login:
            self.login = input('Enter login: ')

        if not self.password:
            self.password = input('Enter password: ')

        # Execute query.
        insertRecord = """insert into
            data_source (data_source, data_source_type_id, connection_string, login, password)
            values ('{}','{}','{}','{}','{}');""".format(
            self.name, dataSourceTypeId, self.connectionString, self.login, self.password
        )
        with Database() as connection:
            connection.executeQuery(insertRecord)

        return(True)

    def update(self, newName=None):
        """Update a data source."""
        log.info('Update data source')

        # If no data source name is provided ask for it.
        if not self.name:
            self.name = input('Enter data source name: ')

        # Verify data source exist.
        data = self.get()
        if len(data) != 0:
            dataSourceId = data[0]['data_source_id']
        else:
            log.info('Data source {} does not exist'.format(self.name))
            self.name = None
            return(False)

        # If no data source type name is provided ask for it.
        if not self.type:
            self.type = input('Enter new data source type (Database, Api, File): ')

        # Verify data source type exist.
        dataSourceType = DataSourceType(self.type)
        data = dataSourceType.get()
        if len(data) != 0:
            dataSourceTypeId = data[0]['data_source_type_id']
        else:
            log.info('Data source type {} does not exist'.format(self.type))
            self.type = None
            return(False)

        # If other attributes are not provided ask for them.
        if not newName:
            newName = input('Enter new data source name: ')

        if not self.connectionString:
            self.connectionString = input('Enter new connection string: ')

        if not self.login:
            self.login = input('Enter new login: ')

        if not self.password:
            self.password = input('Enter new password: ')

        # Execute query.
        updateRecord = """update data_source set data_source='{}', data_source_type_id='{}',
                          connection_string='{}', login='{}', password='{}',
                          last_updated_date=strftime('%Y-%m-%d %H:%M:%f', 'now')
                          where data_source_id='{}';""".format(
            newName, dataSourceTypeId, self.connectionString,
            self.login, self.password, dataSourceId
        )
        with Database() as connection:
            connection.executeQuery(updateRecord)

        # Update data source type name attribute to new name.
        self.name = newName
        return(True)

    def delete(self):
        """Delete a data source"""
        log.info('Delete data source')

        # If no data source name is provided ask for it.
        if not self.name:
            self.name = input('Enter data source name: ')

        # Verify data source exist.
        data = self.get()
        if len(data) == 0:
            log.info('Data source {} does not exist'.format(self.name))
            self.name = None
            return(False)

        # Verify if data source is used by indicators
        selectRecord = "select indicator from indicator where data_source_id='{}';".format(data[0]['data_source_id'])
        with Database() as connection:
            indicator = connection.executeQuery(selectRecord)
            if len(indicator) != 0:
                log.info('Data source {} is used by the following indicators and cannot be deleted: {}'.format(
                    self.name, indicator
                ))
                return(False)

        # Confirm and execute query.
        if input('This will delete the data source type. Are you sure (Y/n): ') == 'Y':
            deleteDataSource = "delete from data_source where data_source_id='{}';".format(data[0]['data_source_id'])
            with Database() as connection:
                connection.executeQuery(deleteDataSource)

        # Update data source name attribute to none since it got deleted.
        self.name = None
        return(True)
