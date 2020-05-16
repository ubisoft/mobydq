---
layout: page
title: Data Source Connection Strings
use-site-title: true
---

The following page provides examples of data source connection strings. MobyDQ connects to relational databases using [pyodbc](https://github.com/mkleehammer/pyodbc/wiki). More examples of connection strings are available in pyodbc documentation.

> Note: In case a data source requires a login and password, those **should not** be written in the connection string but rather in their dedicated fields in the web application. MobyDQ will automatically add them to the connection string when connecting to the data source. You can refer to the sample data sources created when initializing MobyDQ.

- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
  - [Cloudera Hive](#cloudera-hive)
  - [Hortonworks Hive](#hortonworks-hive)
  - [Impala](#impala)
  - [MariaDB](#mariadb)
  - [Microsoft SQL Server](#microsoft-sql-server)
  - [MySQL](#mysql)
  - [Oracle](#oracle)
  - [PostgreSQL](#postgresql)
  - [Snowflake](#snowflake)
  - [SQLite](#sqlite)
  - [Teradata](#teradata)

# Troubleshooting

Troubleshooting connectivity to a data source can be quite complex because of all the possible network specificities, database servers configurations and various authentication mechanisms (Active Directory, Kerberos, direct database authentication, etc.). You can use the following code snippet in order to test a connectiong string and the connectivity to a data source.

```shell
# Run mobydq-scripts Docker container and connect to it in interactive mode
$ docker run -it --rm --network mobydq_network mobydq-scripts sh

# Start the Python interpreter inside the container
$ python
```

Paste the following code in the Python interpreter, make sure you update the connection string parameters, uid, pwd, etc. If no error is returned and you can print the `('Hello World!',)` tuple successfully it means the connection worked.

```python
>>> import pyodbc
>>> connection_string = "driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;uid=sa;pwd=1234-abcd"
>>> connection = pyodbc.connect(connection_string)
>>> cursor = connection.cursor()
>>> query = "SELECT 'Hello World!';"
>>> cursor.execute(query)
>>> row = cursor.fetchone()
>>> print(row)
```

---

# Examples

## Cloudera Hive

```
driver={Cloudera Hive};host=db-hive;port=10000;
```

---

## Hortonworks Hive

```
Driver={Hortonworks Hive};host=db-hive;port=10000;
```

---

## Impala

```
To be documented
```

---

## MariaDB

```
driver={MariaDB Unicode};server=db-mariadb;port=3306;database=star_wars;
```

---

## Microsoft SQL Server

Connection string for database authentication using a database user.

```
driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;
```

Connection string for Active Directory authentication using a Windows user. The user must be supplied in the dedicated field in the web application with the format `domain\user`.

```
driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;usentlmv2=yes;
```

---

## MySQL

```
driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;
```

---

## Oracle

```
driver={Oracle};dbq=db-oracle:1521/orclcdb;
```

---

## PostgreSQL

```
driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;
```

---

## Snowflake

```
driver={Snowflake};server=account-name.snowflakecomputing.com;port=443;
```

---

## SQLite

```
./star_wars.db
```

---

## Teradata

```
driver={Teradata 64};dbcname=db-teradata;defaultdatabase=star_wars;charset=utf8;
```
