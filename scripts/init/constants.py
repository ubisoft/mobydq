"""Contain constants Ids and labels."""
from enum import Enum


class DataSourceType(Enum):
    """Data source type Ids."""
    HIVE_ID = 1
    IMPALA_ID = 2
    MARIADB_ID = 3
    MSSQL_ID = 4
    MYSQL_ID = 5
    ORACLE_ID = 6
    POSTGRESQL_ID = 7
    SQLITE_ID = 8
    TERADATA_ID = 9
