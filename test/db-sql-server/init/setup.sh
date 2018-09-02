# Wait for SQL Server to be started
sleep 30s

# Run the setup script to create the database
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -d master -i database.sql
