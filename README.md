# Work In Progress /!\
Looking for contributors, in particular to build a lightweight web interface on top of the API.
The more the merrier!

# Data Quality Framework
The objective of this framework is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use. It has been developed as an internal project at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. Its open source version has been reworked to remove technical dependencies with commercial softwares.

![Data pipeline](/doc/data_pipeline.png)

## Getting Started
Skip the bla bla and run your data quality indicators immediately by following the [Getting Started](https://github.com/alexisrolland/data-quality/wiki/Getting-Started) guide. However, for a better understanding of the framework, its concepts and how it works, we recommend you refer to the documentation below.

## Documentation
The complete documentation is available on [Github wiki](https://github.com/alexisrolland/data-quality/wiki).

## Dependencies
This framework has been developed on **Linux** with **Python 3.5** and is powered by the following awesome packages:
* [argparse](https://docs.python.org/3/library/argparse.html)
* [configparser](https://docs.python.org/3/library/configparser.html)
* [flask](http://flask.pocoo.org/)
* [flask_cors](http://flask-cors.readthedocs.io)
* [flask_restplus](http://flask-restplus.readthedocs.io)
* [pandas](http://pandas.pydata.org/)
* [pyodbc](https://github.com/mkleehammer/pyodbc)
* [requests](http://docs.python-requests.org)
* [sqlalchemy](https://www.sqlalchemy.org/)
