FROM python:3.6.6-slim-stretch

# Add dependencies for Python package pyodbc
RUN apt-get update \
    && apt-get install -y g++ unixodbc-dev

# Project files
ARG PROJECT_DIR=/srv/scripts
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Add FreeTDS ODBC driver for Microsoft SQL Server
RUN apt-get install -y tdsodbc

# Add MySQL ODBC driver
#RUN apt-get install -y yum yum-utils \
#    && yum install mysql-connector-odbc

# Add PostgreSQL ODBC driver
RUN apt-get install -y odbc-postgresql

# Update ODBC configuration file
COPY odbcinst.ini /etc/odbcinst.ini
