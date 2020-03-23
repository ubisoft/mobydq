---
layout: page
title: Data Source Connection String Examples
use-site-title: true
---

The following page provides examples of data source connection strings. MobyDQ connects to relational databases using [pyodbc](https://github.com/mkleehammer/pyodbc/wiki). More examples of connection strings are available in pyodbc documentation.

> Note: In case a data source requires a login and password, those **should not** be written in the connection string but rather in their dedicated fields in the web application. MobyDQ will automatically add them to the connection string when connecting to the data source. You can refer to the sample data sources created when initializing MobyDQ.

-   [Hive](#hive)
-   [Impala](#impala)
-   [MariaDB](#mariadb)
-   [Microsoft SQL Server](#microsoft-sql-server)
-   [MySQL](#mysql)
-   [Oracle](#oracle)
-   [PostgreSQL](#postgresql)
-   [Snowflake](#snowflake)
-   [SQLite](#sqlite)
-   [Teradata](#teradata)

---

# Hive

```
driver={Cloudera Hive};host=db-hive;port=10000;
```

---

# Impala

```
To be documented
```

---

# MariaDB

```
driver={MariaDB Unicode};server=db-mariadb;port=3306;database=star_wars;
```

---

# Microsoft SQL Server

```
driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;
```

---

# MySQL

```
driver={MySQL Unicode};server=db-mysql;port=3306;database=star_wars;
```

---

# Oracle

```
driver={Oracle};dbq=db-oracle:1521/orclcdb;
```

---

# PostgreSQL

```
driver={PostgreSQL Unicode};server=db-postgresql;port=5432;database=star_wars;
```

---

# Snowflake

```
driver={Snowflake};server=account-name.snowflakecomputing.com;port=443;
```

---

# SQLite

```
./star_wars.db
```

---

# Teradata

```
driver={Teradata 64};dbcname=db-teradata;defaultdatabase=star_wars;charset=utf8;
```
