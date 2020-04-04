---
layout: page
title: Architecture
use-site-title: true
---

# Architecture Diagram

![Architecture](/mobydq/img/architecture.png)

---

# Database

The database `mobydq` uses [PostgreSQL 11.0](https://www.postgresql.org). It contains configuration data required to execute indicators and stores the result of their executions. The database runs into an independent Docker container named `mobydq-db`.

Note direct access to the database is restricted by default to avoid intrusions. In order to access it directly with a SQL client, you must run the container in development mode with the following command which opens the Docker container port:

```
$ cd mobydq
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d db
```

When running the container in local development mode, the database is accessible on `host: localhost` and `port: 5432`.

---

# GraphQL API

The GraphQL API is used to perform CRUD operations on the database and trigger the execution of data quality indicators. It is powered by the excellent [PostGraphile](https://www.graphile.org/postgraphile) which introspects the database schema to create queries and mutations. The GraphQL API runs into an independent Docker container named `mobydq-graphql`. The interactive documentation GraphiQL is accessible on [https://localhost/graphiql](https://localhost/graphiql).

---

# Web Application

The web application provides a user-friendly interface to configure and monitor indicators. It is built using [React JS](https://reactjs.org/) and runs into an independent Docker container named `mobydq-app`. When running the project locally, it is accessible on [https://localhost](https://localhost).

---

# Web Server

Both the web application and the Flask API are served using an [Nginx](https://www.nginx.com/) web server which ensures requests are sent using SSL encryption. Nginx runs into an independent Docker container named `mobydq-nginx`.

---

# Python Scripts

The execution of data quality indicators is triggered by the GraphQL API. Each batch of indicators runs into an independant ephemeral container.
