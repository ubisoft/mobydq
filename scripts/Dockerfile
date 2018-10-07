FROM python:3.6.6-slim-stretch

# Project files
ARG PROJECT_DIR=/srv/scripts
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./init ./

# Add dependencies for Python package pyodbc
RUN apt-get update \
    && apt-get install -y g++ unixodbc-dev

# Add FreeTDS ODBC driver for Microsoft SQL Server
RUN apt-get install -y tdsodbc

# Add MySQL ODBC driver
RUN tar xvzf ./drivers/mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit.tar.gz \
    && cp ./mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit/lib/libmyodbc8* /usr/lib/x86_64-linux-gnu/odbc/ \
    && rm -R ./mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit

# Add PostgreSQL ODBC driver
RUN apt-get install -y odbc-postgresql

# Add Teradata ODBC driver
RUN apt-get install -y lib32stdc++6 \
    && tar xvzf ./drivers/tdodbc1620__ubuntu_indep.16.20.00.36-1.tar.gz \
    && dpkg -i ./tdodbc1620/tdodbc1620-16.20.00.36-1.noarch.deb \
    && rm -R ./tdodbc1620

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Move ODBC configuration file
RUN mv -f ./odbcinst.ini /etc

# Get build arguments coming from .env file
ARG GRAPHQL_URL
ENV GRAPHQL_URL "$GRAPHQL_URL"
ARG MAIL_HOST
ENV MAIL_HOST "$MAIL_HOST"
ARG MAIL_PORT
ENV MAIL_PORT "$MAIL_PORT"
ARG MAIL_SENDER
ENV MAIL_SENDER "$MAIL_SENDER"

# Create config file to send mails using environment variables
RUN echo "[graphql]" >> ./scripts.cfg \
    && echo "url = $GRAPHQL_URL" >> ./scripts.cfg \
    && echo "" >> ./scripts.cfg \
    && echo "[mail]" >> ./scripts.cfg \
    && echo "host = $MAIL_HOST" >> ./scripts.cfg \
    && echo "port = $MAIL_PORT" >> ./scripts.cfg \
    && echo "sender = $MAIL_SENDER" >> ./scripts.cfg

# Deleting drivers packages
RUN rm -R ./drivers
