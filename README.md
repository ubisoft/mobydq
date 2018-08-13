[![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg?style=flat-square)](https://github.com/alexisrolland/data-quality)
[![GitHub license](https://img.shields.io/github/license/alexisrolland/data-quality.svg?style=flat-square)](https://github.com/alexisrolland/data-quality/blob/master/LICENSE)

**Attention:** Project is currently being reworked to use Docker, PostgreSQL and Postgraphile instead of Flask, SQLAlchemy and Graphene. You're welcome to join the adventure if you wish to contribute, in particular to build a lightweight web app on top of the GraphQL API.

# Data Quality Framework
The objective of this framework is to provide a solution for data engineering teams to automate data quality checks on their data pipeline, capture data quality issues and trigger alerts in case of anomaly, regardless of the data sources they use.

It has been influenced by an internal project developed at [Ubisoft Entertainment](https://www.ubisoft.com) in order to measure and improve the data quality of its Enterprise Data Platform. However, this open source version has been completely reworked from scratch to improve its design, simplify it and remove technical dependencies with commercial software.

![Data pipeline](https://github.com/alexisrolland/data-quality/blob/master/doc/architecture.png)

# Getting Started
Skip the bla bla and run your data quality indicators by following the [Getting Started Guide](https://github.com/alexisrolland/data-quality/wiki/Getting-Started). Refer to the documentation below for a better understanding of the framework, its concepts and how it works.

# Requirements
## Install Docker
Add the Docker repository to your Linux repository. Execute the following commands in a terminal window.
```shellsession
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

Install Docker Community Edition.
```shellsession
$ sudo apt-get update
$ sudo apt-get install docker-ce
```

Add your user to the docker group to setup its permissions. **Make sure to restart your machine after executing this command.**
```shellsession
$ sudo usermod -a -G docker <username>
```

## Install Docker Compose
Execute the following command in a terminal window.
```shellsession
$ sudo apt install docker-compose
```

# Setup Your Instance
To setup your instance of the data quality framework, type the following command in your terminal window.
```shellsession
$ python3 setup.py
```

# Start Your Instance
To start all the services of the data quality framework, execute the following commands in a terminal window. It will automatically create the Docker images and run the Docker containers.
```shellsession
$ cd data-quality
$ docker-compose up
```

The list of services are:
* dq-db
* dq-api
* dq-app

# Documentation
The complete documentation is available on [Github wiki](https://github.com/alexisrolland/data-quality/wiki).

# Run Test Cases
To execute all test cases, change directory to the framework folder and execute the following command:
```shellsession
$ nose2 -v
```
