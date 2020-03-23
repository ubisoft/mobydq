FROM python:3.6.6-slim-stretch

# Project files
ARG PROJECT_DIR=/srv/scripts
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Add dependencies for Python package pyodbc and for Hortonworks Hive ODBC driver
RUN apt-get update \
    && apt-get install -y g++ unixodbc unixodbc-dev \
    && apt-get install -y libsasl2-modules-gssapi-mit libsasl2-modules

# Install Python dependencies
COPY ./init/requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy drivers
COPY ./drivers ./drivers

# Install Cloudera Hive ODBC driver
RUN dpkg -i ./drivers/clouderahiveodbc_2.5.25.1020-2_amd64.deb

# Install FreeTDS ODBC driver for Microsoft SQL Server
RUN apt-get install -y tdsodbc

# Install Hortonworks Hive ODBC driver
RUN dpkg -i ./drivers/hive-odbc-native_2.6.1.1001-2_amd64.deb

# Install MySQL ODBC driver
RUN tar xvzf ./drivers/mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit.tar.gz \
    && cp ./mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit/lib/libmyodbc8* /usr/lib/x86_64-linux-gnu/odbc/ \
    && rm -R ./mysql-connector-odbc-8.0.12-linux-debian9-x86-64bit

# Install Oracle ODBC driver
RUN apt-get install -y alien libaio1 \
    && alien -i ./drivers/oracle-instantclient12.2-*
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/12.2/client64/lib

# Add PostgreSQL ODBC driver
RUN apt-get install -y odbc-postgresql

# Install Snowflake ODBC driver
RUN dpkg -i ./drivers/snowflake-odbc-2.20.4.x86_64.deb

# Install Teradata ODBC driver
RUN apt-get install -y lib32stdc++6 \
    && tar xvzf ./drivers/tdodbc1620__ubuntu_indep.16.20.00.36-1.tar.gz \
    && dpkg -i ./tdodbc1620/tdodbc1620-16.20.00.36-1.noarch.deb \
    && rm -R ./tdodbc1620

# Move ODBC configuration file
COPY ./init/odbcinst.ini /etc

# Get build arguments coming from .env file
ARG MAIL_HOST
ENV MAIL_HOST "$MAIL_HOST"
ARG MAIL_PORT
ENV MAIL_PORT "$MAIL_PORT"
ARG MAIL_SENDER
ENV MAIL_SENDER "$MAIL_SENDER"
ARG MAIL_PASSWORD
ENV MAIL_PASSWORD "$MAIL_PASSWORD"
ARG MAIL_BASE_URL
ENV MAIL_BASE_URL "$MAIL_BASE_URL"

# Create config file to send mails using environment variables
RUN echo "[graphql]" >> ./scripts.cfg \
    && echo "url = http://graphql:5433/graphql" >> ./scripts.cfg \
    && echo "" >> ./scripts.cfg \
    && echo "[mail]" >> ./scripts.cfg \
    && echo "host = $MAIL_HOST" >> ./scripts.cfg \
    && echo "port = $MAIL_PORT" >> ./scripts.cfg \
    && echo "sender = $MAIL_SENDER" >> ./scripts.cfg \
    && echo "password = $MAIL_PASSWORD" >> ./scripts.cfg \
    && echo "base_url = $MAIL_BASE_URL" >> ./scripts.cfg

# Deleting drivers packages
RUN rm -rf ./drivers

# Copy code as late as possible
COPY ./init ./
