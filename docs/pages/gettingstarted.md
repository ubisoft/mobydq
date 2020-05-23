---
layout: page
title: Getting Started
use-site-title: true
---

The following page guides you step by step to setup and run MobyDQ in a **local development environment**. For a deployment to **production**, follow the same steps and refer to the page [Production Deployment](/mobydq/pages/productiondeployment).

-   [Requirements](#requirements)
    -   [Linux](#linux)
    -   [Windows](#windows)
-   [Setup Your Instance](#setup-your-instance)
-   [Run Your Instance](#run-your-instance)

---

# Requirements

## Linux

### Install Docker

Add the Docker repository to your Linux machine, execute the following commands in a terminal window.

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

### Install Docker Compose

Execute the following command in a terminal window.

```shell
$ sudo apt install docker-compose
```

Once the installation is complete, proceed to the following step: [Setup Your Instance](#setup-your-instance)

## Windows

-   If your computer runs on Windows Pro, install Docker Desktop for Windows.
-   If your computer runs on Windows Home, install Docker Toolbox for Windows.

### Install Docker Desktop for Windows (Windows Pro)

Install Docker Community Edition for Windows from the following the URL: [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows). Once the installation is complete, proceed to the following step: [Setup Your Instance](#setup-your-instance)

### Install Docker Toolbox for Windows (Windows Home)

Install Docker Toolbox for Windows from the following the URL: [Docker Toolbox for Windows](https://docs.docker.com/toolbox/overview). Once the installation is complete, proceed to the following step: [Setup Your Instance](#setup-your-instance).

**Using Docker Toolbox default settings requires the project to be in the directory:** `C:/Users/<your_user>/`

---

# Setup Your Instance

## Create Configuration File

Create a text file named `.env` at the root of the repository using the template below. This file is used by Docker Compose to load configuration parameters into environment variables. Make sure to update the `postgres` user password for both `POSTGRES_PASSWORD` and `DATABASE_URL` parameters.

```ini
# DB
# Parameters used by mobydq-db container to create the PostgreSQL database
POSTGRES_DB=mobydq
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me

# GRAPHQL
# Parameters used by mobydq-graphql container to connect to the database
GRAPHQL_DATABASE_URL=postgres://postgres:change_me@db:5432/mobydq
GRAPHQL_PORT=5433
GRAPHQL_SECRET_KEY=change_me

# SCRIPTS
# Parameters used by mobydq-scripts container to send e-mails
# If your Gmail account uses 2-Step Verification, you need to create an App password: https://support.google.com/accounts/answer/185833
# You might not need a password if you use a private SMTP server without authentication
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_SENDER=change_me@gmail.com
MAIL_PASSWORD=change_me
MAIL_BASE_URL=https://localhost
```

## Create SSL Certificate

The API and the web app are served by an Nginx web server with SSL encryption (https). In order to encrypt http requests when running the project locally, you must generate a self-signed certificate and its corresponding private key. You can do it using this docker container: [Docker-OpenSSL](https://github.com/alexisrolland/docker-openssl)

Execute the following commands to build the Docker image:

```shell
# Clone repository
$ git clone https://github.com/alexisrolland/docker-openssl.git
$ cd docker-openssl

# Build Docker image
$ docker build -t docker-openssl:latest .

# Run Docker container in interactive mode
# Make sure you replace `<your_path>` with your target folder, this is where files will be created.

# If you are on Linux
$ docker run -it --rm -v "/<your_path>/mobydq/nginx/config:/openssl-certs" docker-openssl

# For Docker Desktop (Windows Pro)
$ docker run -it --rm -v "C:\<your_path>\mobydq\nginx\config:/openssl-certs" docker-openssl

# For Docker Toolbox (Windows Home)
$ docker run -it --rm -v "/c/<your_path>/mobydq/nginx/config:/openssl-certs" docker-openssl
```

Generate the certificate file and its private key:

```shell
# Generate cert.pem and key.pem files
$ req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

You will be prompted a couple of questions which you can answer following this example:

```
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:Shanghai
Locality Name (eg, city) []:Shanghai
Organization Name (eg, company) [Internet Widgits Pty Ltd]:MobyDQ
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:
```

## Build Docker Images

Go to the project root and execute the following command in your terminal window.

```shell
$ cd mobydq
$ docker-compose build --no-cache
```

---

# Run Your Instance

## Run Docker Containers

To start all the Docker containers as deamons, go to the project root and execute the following command in your terminal window.

```shell
$ cd mobydq
$ docker-compose up -d db graphql app nginx
```

Individual components can be accessed at the following addresses:

<table>
 <tr>
  <th>
   Component
  </th>
  <th>
   Docker on Linux / Windows Pro
  </th>
  <th>
   Docker on Windows Home
  </th>
 </tr>
 <tr>
  <td>
   Web application
  </td>
  <td>
   <a href="https://localhost">https://localhost</a>
  </td>
  <td>
   <a href="https://your_docker_machine_ip">https://your_docker_machine_ip</a>
  </td>
 </tr>
 <tr>
  <td>
   GraphQL API Documentation
  </td>
  <td>
   <a href="https://localhost/graphiql">https://localhost/graphiql</a>
  </td>
  <td>
   <a href="https://your_docker_machine_ip/graphiql">https://your_docker_machine_ip/graphiql</a>
  </td>
 </tr>
 <tr>
  <td>
   GraphQL API
  </td>
  <td>
   <a href="https://localhost/graphql">https://localhost/graphql</a>
  </td>
  <td>
   <a href="https://your_docker_machine_ip/graphql">https://your_docker_machine_ip/graphql</a>
  </td>
 </tr>
 <tr>
  <td>
   PostgreSQL Database
  </td>
  <td>
   host: localhost, port: 5432
  </td>
  <td>
   host: your_docker_machine_ip, port: 5432
  </td>
 </tr>
</table>

Note access to the PostgreSQL database is restricted by default to avoid intrusions. In order to access it directly from outside the Docker network, you must run it in development mode with the following command to open its port:

```shell
$ cd mobydq
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d db
```
