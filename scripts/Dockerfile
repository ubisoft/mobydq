FROM python:3.6.6-slim-stretch

# Add dependencies for Python package pyodbc
RUN apt-get update \
    && apt-get install -y g++ unixodbc-dev

# Project files
ARG PROJECT_DIR=/srv/scripts
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./init ./

# Move ODBC configuration file
RUN mv -f ./odbcinst.ini /etc

# Get build arguments coming from .env file
ARG MAIL_HOST
ENV MAIL_HOST "$MAIL_HOST"
ARG MAIL_PORT
ENV MAIL_PORT "$MAIL_PORT"
ARG MAIL_SENDER
ENV MAIL_SENDER "$MAIL_SENDER"

# Create config file to send mails using environment variables
RUN echo "[mail]" >> ./scripts.cfg \
    && echo "host = $MAIL_HOST" >> ./scripts.cfg \
    && echo "port = $MAIL_PORT" >> ./scripts.cfg \
    && echo "sender = $MAIL_SENDER" >> ./scripts.cfg

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Add FreeTDS ODBC driver for Microsoft SQL Server
RUN apt-get install -y tdsodbc

# Add MySQL ODBC driver
# RUN apt-get install -y yum yum-utils \
#    && yum install mysql-connector-odbc

# Add PostgreSQL ODBC driver
RUN apt-get install -y odbc-postgresql
