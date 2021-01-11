# MobyDQ

![License](https://img.shields.io/github/license/mobydq/mobydq.svg "Apache-2.0")
![tests](https://github.com/ubisoft/mobydq/workflows/tests/badge.svg)

![MobyDQ](https://ubisoft.github.io/mobydq/img/logo/mobydq_logo_black_horizontal_small.png)

**MobyDQ** is a tool for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

This tool has been inspired by an internal project developed at <a href="https://www.ubisoft.com">Ubisoft Entertainment</a> in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been reworked to improve its design, simplify it and remove technical dependencies with commercial software.

![Data pipeline](https://ubisoft.github.io/mobydq/img/data_pipeline.png)

# Getting Started

Skip the bla bla and run your data quality indicators by following the [Getting Started page](https://ubisoft.github.io/mobydq/pages/gettingstarted/). The complete documentation is also available on Github Pages: [https://ubisoft.github.io/mobydq](https://ubisoft.github.io/mobydq).

# Screenshots

Some screenshot of the web application to give you a taste of how it's like.

![Demo](https://ubisoft.github.io/mobydq/img/demo_screenshot.png)

# Run Dev

Run MobyDQ in development mode with the following command:

```shell
$ cd mobydq
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up db graphql app nginx
```

# Run Prod

Run MobyDQ in production mode with the following command. The argument `-d` is to run containers in the background as daemons.

```shell
$ cd mobydq
$ docker-compose up -d db graphql app nginx
```

# Run Tests

You can run tests using the following commands:

```shell
$ cd mobydq

# Start test database instances
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d db graphql
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d db-cloudera db-mysql db-mariadb db-postgresql db-sql-server

# Run tests
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml up test-db test-scripts

# Run linter
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml build test-scripts test-lint-python
$ docker run --rm mobydq-test-lint-python pylint scripts test
```

# Dependencies

## Docker Images

-   [postgres](https://hub.docker.com/_/postgres/) (tag: 11.0-alpine)
-   [python](https://hub.docker.com/_/python/) (tag: 3.6.6-slim-stretch)
-   [node](https://hub.docker.com/_/node/) (tag: alpine)
-   [nginx](https://hub.docker.com/_/nginx/) (tag: alpine)

## Python Packages

-   [jinja2](http://jinja.pocoo.org) (2.10.1)
-   [numpy](http://www.numpy.org) (1.14.0)
-   [pandas](https://pandas.pydata.org) (0.23.0)
-   [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.23)
-   [requests](http://docs.python-requests.org) (2.20.0)

## JavaScript Packages

-   To be documented
