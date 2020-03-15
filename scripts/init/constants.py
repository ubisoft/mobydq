"""Contain constants Ids and labels."""
# pylint: disable=R0903


class DataSourceType:
    """Data source type Ids."""

    CLOUDERA_HIVE_ID = 1
    CLOUDERA_IMPALA_ID = 2
    MARIADB_ID = 3
    MSSQL_ID = 4
    MYSQL_ID = 5
    ORACLE_ID = 6
    POSTGRESQL_ID = 7
    SQLITE_ID = 8
    TERADATA_ID = 9
    SNOWFLAKE_ID = 10
    HORTONWORKS_HIVE_ID = 11


class IndicatorType:
    """Indicator type Ids."""

    COMPLETENESS = 1
    FRESHNESS = 2
    LATENCY = 3
    VALIDITY = 4
