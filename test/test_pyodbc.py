import pyodbc
print('Start test')
conn = 'driver={PostgreSQL Unicode};server=172.21.0.3;port=5432;database=data_quality;pwd=password;uid=postgres;'
print('Connection string set')
connection = pyodbc.connect(conn)
print('Success')
