[![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg?style=flat-square)](https://github.com/alexisrolland/data-quality)
[![GitHub license](https://img.shields.io/github/license/alexisrolland/data-quality.svg?style=flat-square)](https://github.com/alexisrolland/data-quality/blob/master/LICENSE)


**Work In Progress:** Looking for contributors, in particular to build a lightweight web app on top of the API.

# Data Quality Framework
The objective of this framework is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use. It has been developed as an internal project at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. Its open source version has been reworked to remove technical dependencies with commercial softwares.

![Data pipeline](/doc/data_pipeline.png)

# Requirements
## Python
This framework has been developed on **Linux** with **Python 3.5** and is powered by the following awesome packages. To install dependencies, open a terminal window, change directory to the framework folder and execute the following command:

`$ pip3 install -r requirements.txt`

The following Python packages will be installed:
* [flask](http://flask.pocoo.org/) (0.12.2)
* [flask_cors](http://flask-cors.readthedocs.io) (3.0.3)
* [flask_restplus](http://flask-restplus.readthedocs.io) (0.10.1)
* [nose2](http://nose2.readthedocs.io/en/latest/index.html) (0.7.0)
* [pandas](http://pandas.pydata.org/) (0.21.0)
* [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.21)
* [requests](http://docs.python-requests.org) (2.9.1)
* [sqlalchemy](https://www.sqlalchemy.org/) (1.1.14)

## ODBC Drivers
This framework uses **pyodbc** to connect to various databases. For each type of database engine you wish to connect, it requires to have the corresponding ODBC drivers installed on your machine.

# Getting Started
Skip the bla bla and run your data quality indicators by following the [Getting Started](https://github.com/alexisrolland/data-quality/wiki/Getting-Started) guide. Refer to the documentation below for a better understanding of the framework, its concepts and how it works.

# Documentation
The complete documentation is available on [Github wiki](https://github.com/alexisrolland/data-quality/wiki).

# Run Test Cases
To execute all test cases, change directory to the framework folder and execute the following command:

`$ nose2 -v`
