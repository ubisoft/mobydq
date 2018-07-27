[![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg?style=flat-square)](https://github.com/alexisrolland/data-quality)
[![GitHub license](https://img.shields.io/github/license/alexisrolland/data-quality.svg?style=flat-square)](https://github.com/alexisrolland/data-quality/blob/master/LICENSE)

**Attention:** Project is currently being reworked to use Docker, PostgreSQL and Postgraphile instead of Flask, SQLAlchemy and Graphene. Check the [project backlog](https://github.com/alexisrolland/data-quality/projects/1) for more information or contact me directly. You're welcome to join the adventure if you wish to contribute.

**Work In Progress:** Looking for contributors, in particular to build a lightweight web app on top of the GraphQL API.

# Data Quality Framework
The objective of this framework is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

It has been influenced by an internal project developed at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been completely reworked from scratch to improve its design, simplify it and remove technical dependencies with commercial softwares.

![Data pipeline](/doc/data_pipeline.png)

# Getting Started
Skip the bla bla and run your data quality indicators by following the [Getting Started Guide](https://github.com/alexisrolland/data-quality/wiki/Getting-Started). Refer to the documentation below for a better understanding of the framework, its concepts and how it works.

# Requirements
## ODBC Drivers
This framework has been developed on **Linux Ubuntu**. It uses ODBC connections to query the different databases on which you want to perform data quality checks. As a matter of fact, it requires to install [UnixODBC](http://www.unixodbc.org/) on your machine. Open a terminal window and execute the following command:

`$ sudo apt-get install unixodbc-dev`

Note that for each type of database engine you wish to connect, it requires to install the corresponding ODBC drivers on your machine.

## Python
This framework has been developed with **Python 3.5** and is powered by the following third party packages. To install them, open a terminal window, change directory to the framework folder and execute the following command:

`$ pip3 install -r requirements.txt`

The following Python packages will be installed:
* [cryptography](https://cryptography.io) (2.1.3)
* [flask](http://flask.pocoo.org) (0.12.2)
* [flask_cors](http://flask-cors.readthedocs.io) (3.0.3)
* [flask_graphql](https://pypi.python.org/pypi/Flask-GraphQL) (1.4.1)
* [graphene](http://graphene-python.org/) (2.0.1)
* [graphene_sqlalchemy](https://pypi.python.org/pypi/graphene-sqlalchemy/2.0.0) (2.0.0)
* [jinja2](https://pypi.python.org/pypi/Jinja2) (2.10)
* [nose2](http://nose2.readthedocs.io) (0.7.0)
* [pandas](http://pandas.pydata.org) (0.21.0)
* [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.21)
* [requests](http://docs.python-requests.org) (2.9.1)
* [sqlalchemy](https://www.sqlalchemy.org) (1.1.14)

# Setup Your Instance
To setup your instance of the data quality framework, type the following command in your terminal window.

```shellsession
$ python3 setup.py
```

# Start the GraphQL API
You can start the API with the following command:

```shellsession
$ python3 api/run.py
```

# Start the Web Application
**Work in progress**

You can start the web app with the following command:

```shellsession
$ python3 app/run.py
```

# Documentation
The complete documentation is available on [Github wiki](https://github.com/alexisrolland/data-quality/wiki).

# Run Test Cases
To execute all test cases, change directory to the framework folder and execute the following command:

`$ nose2 -v`
