# MobyDQ
![License](https://img.shields.io/github/license/mobydq/mobydq.svg "Apache-2.0")

[![CircleCI](https://circleci.com/gh/mobydq/mobydq/tree/master.svg?style=shield)][CircleCI]

[CircleCI]: https://circleci.com/gh/mobydq/mobydq/tree/master (CircleCI)

**MobyDQ** is a tool for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

![Data pipeline](https://mobydq.github.io/img/data_pipeline.png)

This tool has been inspired by an internal project developed at <a href="https://www.ubisoft.com">Ubisoft Entertainment</a> in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been reworked to improve its design, simplify it and remove technical dependencies with commercial software.


# Getting Started
Skip the bla bla and run your data quality indicators by following the [Getting Started page](https://mobydq.github.io/pages/gettingstarted/). The complete documentation is also available on Github Pages: [https://mobydq.github.io](https://mobydq.github.io).


# Run Tests
You can run all tests locally using the following commands:
```shell
$ cd mobydq
$ # Backend
$ test/run-tests.sh
$ # Frontend
$ app/run-container.sh npm run test
```

# Run Linter
Depending on the used editor, eslint and pylint can be integrated.
You can run all linters locally using the following commands:
```shell
$ cd mobydq
$ # Backend
$ test/run-linter.sh
$ # Frontend
$ app/run-container.sh npm run lint
```


# Dependencies
## Docker Images
The containers run by `docker-compose` have dependencies with the following Docker images:
* [postgres](https://hub.docker.com/_/postgres/) (tag: 10.4-alpine)
* [graphile/postgraphile](https://hub.docker.com/r/graphile/postgraphile/) (tag: latest)
* [python](https://hub.docker.com/_/python/) (tag: 3.6.6-alpine3.8)
* [python](https://hub.docker.com/_/python/) (tag: 3.6.6-slim-stretch)


## Python Packages
* [docker](https://docker-py.readthedocs.io) (3.5.0)
* [flask](http://flask.pocoo.org) (1.0.2)
* [flask_restplus](https://flask-restplus.readthedocs.io) (0.11.0)
* [flask_cors](https://flask-cors.readthedocs.io) (3.0.6)
* [graphql_py](https://pypi.org/project/graphql-py) (0.7.1)
* [jinja2](http://jinja.pocoo.org) (2.10.0)
* [numpy](http://www.numpy.org) (1.14.0)
* [pandas](https://pandas.pydata.org) (0.23.0)
* [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.23)
* [requests](http://docs.python-requests.org) (2.20.0)
* [requests_oauthlib](https://requests-oauthlib.readthedocs.io)(1.0.0)
