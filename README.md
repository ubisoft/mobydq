[![GitHub license](https://img.shields.io/github/license/alexisrolland/data-quality.svg?style=flat-square)](https://github.com/alexisrolland/data-quality/blob/master/LICENSE)

**Attention:** Project is currently being reworked to use Docker, PostgreSQL, Postgraphile, Flask and React.js. Python packages SQLAlchemy and Graphene will be removed. You're welcome to join the adventure if you wish to contribute, in particular to build a lightweight web app on top of the GraphQL API.

# Data Quality Framework
The objective of this tool is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

It has been influenced by an internal project developed at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been completely reworked from scratch to improve its design, simplify it and remove technical dependencies with commercial software.

![Data pipeline](https://github.com/alexisrolland/data-quality/blob/development/doc/data_pipeline.png)

# Getting Started
Skip the bla bla and run your data quality indicators by following the [Getting Started Guide](https://github.com/alexisrolland/data-quality/wiki/Getting-Started). The complete documentation is also available on [Github wiki](https://github.com/alexisrolland/data-quality/wiki) if you wish to better understanding the tool, its concepts and how it works.

# Requirements
## Install Docker
This tool has been fully containerized with Docker to ensure easy deployment and portability. To add the Docker repository to your Linux machine, execute the following commands in a terminal window.
```shell
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

Install Docker Community Edition.
```shell
$ sudo apt-get update
$ sudo apt-get install docker-ce
```

Add your user to the docker group to setup its permissions. **Make sure to restart your machine after executing this command.**
```shell
$ sudo usermod -a -G docker <username>
```

## Install Docker Compose
Execute the following command in a terminal window.
```shell
$ sudo apt install docker-compose
```

# Setup Your Instance
## Create Configuration Files
Based on the template below, create a text file named `.env` at the root of the project. This file is used by Docker Compose to load configuration parameters into environment variables. This is typically used to manage file paths, logins, passwords, etc. Make sure to update the `postgres` user password in both `POSTGRES_PASSWORD` and `DATABASE_URL` parameters.
```ini
# DB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# GRAPHQL
DATABASE_URL=postgres://postgres:password@db:5432/data_quality

# SCRIPTS
API_URL=http://graphql:5433/graphql
MAIL_HOST=smtp.server.org
MAIL_PORT=25
MAIL_SENDER=change@me.com
```

Based on the template below, create a text file named `.env.app` in `./app/` folder.
```ini
# APP
BASE_URL=http://api.base.url
```

## Create Docker Network
This custom network is used to connect the different containers. It's used in particular to connect the ephemeral containers ran when executing batches of indicators.
```shell
$ docker network create data-quality-network
```

## Create PostgreSQL Data Volume
Due to Docker compatibility issues on Windows machines, we recommend to manually create a Docker volume instead of directly mounting external folders in `docker-compose.yml`. This volume will be used to persist the data stored in the PostgreSQL database. Execute the following command.
```shell
$ docker volume create data-quality-db-volume
```

## Build Docker Images
Go to the project repository and execute the following commands in your terminal window to build the Docker images.
```shell
$ cd data-quality
$ docker-compose build --no-cache
```

## Run Docker Containers
From the project repository, start all the Docker containers as deamons. Execute the following command in a terminal window.
```shell
$ docker-compose up db graphql api app -d
```

# Dependencies
## Docker Images
The containers run by `docker-compose` have dependencies with the following Docker images:
* [postgres](https://hub.docker.com/_/postgres/) (tag: 10.4-alpine)
* [graphile/postgraphile](https://hub.docker.com/r/graphile/postgraphile/) (tag: latest)
* [python](https://hub.docker.com/_/python/) (tag: 3.6.6-alpine3.8)
* [python](https://hub.docker.com/_/python/) (tag: 3.6.6-slim-stretch)

## Python Packages
The container `data-quality-api` has dependencies with the following Python packages:
* [docker](https://docker-py.readthedocs.io) (3.5.0)
* [flask](http://flask.pocoo.org) (1.0.2)
* [flask_restplus](https://flask-restplus.readthedocs.io) (0.11.0)
* [requests](http://docs.python-requests.org) (2.19.1)

The container `data-quality-scripts` has dependencies with the following Python packages:
* [jinja2](http://jinja.pocoo.org) (2.10.0)
* [numpy](http://www.numpy.org) (1.14.0)
* [pandas](https://pandas.pydata.org) (0.23.0)
* [pyodbc](https://github.com/mkleehammer/pyodbc) (4.0.23)
* [requests](http://docs.python-requests.org) (2.19.1)

# Run Test Cases
To execute all test cases, execute following command from the project repository:
```shell
$ cd data-quality/test
$ to be documented
```
