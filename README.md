# Data Quality Framework
The objective of this framework is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use. It has been developed as an internal project at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. Its open source version has been reworked to remove technical dependencies with commercial softwares.

![Data pipeline](/doc/data_pipeline.png)

## Documentation
Full documentation is available on [Github Wiki](https://github.com/alexisrolland/data-quality/wiki).

## Dependencies
This framework has been developed on **Python 3.5** and is powered by the following awesome packages:
* [argparse](https://docs.python.org/3/library/argparse.html)
* [configparser](https://docs.python.org/3/library/configparser.html)
* [pandas](http://pandas.pydata.org/)
* [pyodbc](https://github.com/mkleehammer/pyodbc)
* [sqlalchemy](https://www.sqlalchemy.org/)
