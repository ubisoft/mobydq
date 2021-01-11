---
layout: page
title: Data Sources
use-site-title: true
---

# Data Source

Data sources are systems containing or exposing data like relational databases or APIs. The `data_source` table stores information about the systems to which MobyDQ can connect to compute indicators.

> Note: MobyDQ only supports connections to data source types listed below: [Data Source Type](#data-source-type). You can refer to [data souce connection strings examples](/mobydq/pages/datasourceconnectionstrings/) to setup your data sources.

**Table:** `data_source`<br/>

<table>
  <tr>
    <th>Attribute</th><th>Type</th><th>Description</th>
  </tr>
  <tr>
    <td>id</td><td>Integer</td><td>Unique identifier of the data source, used as a primary key.</td>
  </tr>
  <tr>
    <td>name</td><td>Text</td><td>Name of the data source, must be unique.</td>
  </tr>
  <tr>
    <td>connection_string</td><td>Text</td><td>Connection string used to connect to the data source.</td>
  </tr>
  <tr>
    <td>login</td><td>Text</td><td>Login used to connect to the data source.</td>
  </tr>
  <tr>
    <td>password</td><td>Text</td><td>Password used to connect to the data source.</td>
  </tr>
  <tr>
    <td>connectivity_status</td><td>Text</td><td>Status to indicate if the connection to the data source works.</td>
  </tr>
  <tr>
    <td>created_date</td><td>Timestamp</td><td>Record created date.</td>
  </tr>
  <tr>
    <td>updated_date</td><td>Timestamp</td><td>Record last updated date.</td>
  </tr>
  <tr>
    <td>created_by_id</td><td>Integer</td><td>Foreign key of the user table, to indicate which user created the record.</td>
  </tr>
  <tr>
    <td>updated_by_id</td><td>Integer</td><td>Foreign key of the user table, to indicate which user updated the record.</td>
  </tr>
  <tr>
    <td>user_group_id</td><td>Integer</td><td>Foreign key of the user_group table, to indicate to which user group the record belongs to.</td>
  </tr>
  <tr>
    <td>data_source_type_id</td><td>Integer</td><td>Foreign key of the data_source_type table, to indicate which type is the data source.</td>
  </tr>
</table>

**Examples of Data Source:**
More examples of data sources are available in the sample dataset when installing MobyDQ.

<table>
  <tr>
    <th>Attribute</th><th>Value</th>
  </tr>
  <tr>
    <td>name</td><td>dq_example_microsoft_sql_server</td>
  </tr>
  <tr>
    <td>connection_string</td><td>driver={FreeTDS};server=db-sql-server;port=1433;database=star_wars;tds_version=8.0;</td>
  </tr>
  <tr>
    <td>login</td><td>sa</td>
  </tr>
  <tr>
    <td>connectivity_status</td><td>Success</td>
  </tr>
  <tr>
    <td>data_source_type_id</td><td>4</td>
  </tr>
</table>

---

# Data Source Type

Data source types describe the type of systems MobyDQ can connect to.

**Table:** `data_source_type`<br/>

<table>
  <tr>
    <th>Attribute</th><th>Type</th><th>Description</th>
  </tr>
  <tr>
    <td>id</td><td>Integer</td><td>Unique identifier of the type of data source, used as a primary key.</td>
  </tr>
  <tr>
    <td>name</td><td>Text</td><td>Type of data source, must be unique.</td>
  </tr>
  <tr>
    <td>created_date</td><td>Timestamp</td><td>Record created date.</td>
  </tr>
  <tr>
    <td>updated_date</td><td>Timestamp</td><td>Record last updated date.</td>
  </tr>
  <tr>
    <td>created_by_id</td><td>Integer</td><td>Foreign key of the user table, to indicate which user created the record.</td>
  </tr>
  <tr>
    <td>updated_by_id</td><td>Integer</td><td>Foreign key of the user table, to indicate which user updated the record.</td>
  </tr>
</table>

**List of Data Source Type Values**

<table>
  <tr>
    <th>id</th><th>name</th>
  </tr>
  <tr>
    <td>1</td><td>Cloudera Hive</td>
  </tr>
  <tr>
    <td>2</td><td>Cloudera Impala (not support yet)</td>
  </tr>
  <tr>
    <td>3</td><td>MariaDB</td>
  </tr>
  <tr>
    <td>4</td><td>Microsoft SQL Server</td>
  </tr>
  <tr>
    <td>5</td><td>MySQL</td>
  </tr>
  <tr>
    <td>6</td><td>Oracle</td>
  </tr>
  <tr>
    <td>7</td><td>PostgreSQL</td>
  </tr>
  <tr>
    <td>8</td><td>SQLite</td>
  </tr>
  <tr>
    <td>9</td><td>Teradata</td>
  </tr>
  <tr>
    <td>10</td><td>Snowflake</td>
  </tr>
  <tr>
    <td>11</td><td>Hortonworks Hive</td>
  </tr>
</table>
