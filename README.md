# MobyDQ

![License](https://img.shields.io/github/license/mobydq/mobydq.svg "Apache-2.0")
[![CircleCI](https://circleci.com/gh/mobydq/mobydq/tree/master.svg?style=shield)][circleci]

[circleci]: https://circleci.com/gh/mobydq/mobydq/tree/master "CircleCI"

**MobyDQ** is a tool for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

![Data pipeline](https://mobydq.github.io/img/data_pipeline.png)

This tool has been inspired by an internal project developed at <a href="https://www.ubisoft.com">Ubisoft Entertainment</a> in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been reworked to improve its design, simplify it and remove technical dependencies with commercial software.

# Getting Started

Skip the bla bla and run your data quality indicators by following the [Getting Started page](https://mobydq.github.io/pages/gettingstarted/). The complete documentation is also available on Github Pages: [https://mobydq.github.io](https://mobydq.github.io).

# Screenshots

Some screenshot of the web application to give you a taste of how it's like.

![Edit Indicator](https://mobydq.github.io/img/edit_indicator.png)

# Run Dev

Run MobyDQ in development mode with the following command:

```shell
$ cd mobydq
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up db graphql api app nginx
```

# Run Prod

Run MobyDQ in production mode with the following command. The argument `-d` is to run containers in the background as daemons.

```shell
$ cd mobydq
$ docker-compose up -d db graphql api app nginx
```

# Run Tests

You can run tests using the following commands:

```shell
$ cd mobydq

# Start test database instances
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d db graphql api
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d db-hive db-mysql db-mariadb db-postgresql db-sql-server

# Run tests
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up test-db test-api test-scripts

# Run linter
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml build test-scripts test-lint-python
$ docker run --rm mobydq-test-lint-python pylint scripts test api/api.py api/proxy api/health api/security
```

# Dependencies

## Docker Images

The containers run by `docker-compose` have dependencies with the following Docker images:

-   [postgres](https://hub.docker.com/_/postgres/) (tag: 11.0-alpine)
-   [graphile/postgraphile](https://hub.docker.com/r/graphile/postgraphile/) (tag: latest)
-   [python](https://hub.docker.com/_/python/) (tag: 3.6.6-alpine3.8)
-   [python](https://hub.docker.com/_/python/) (tag: 3.6.6-slim-stretch)
-   [nginx](https://hub.docker.com/_/nginx/) (tag: latest)

## Python Packages

-   [docker](https://docker-py.readthedocs.io) (3.5.0)
-   [flask](http://flask.pocoo.org) (1.0.2)
-   [flask_cors](https://flask-cors.readthedocs.io) (3.0.8)
-   [flask_restplus](https://flask-restplus.readthedocs.io) (0.11.0)
-   [graphql_py](https://pypi.org/project/graphql-py) (0.7.1)
-   [jinja2](http://jinja.pocoo.org) (2.10.1)
-   [numpy](http://www.numpy.org) (1.14.0)
-   [pandas](https://pandas.pydata.org) (0.23.0)
-   [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.23)
-   [requests](http://docs.python-requests.org) (2.20.0)
