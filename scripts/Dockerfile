FROM python:3.6.6-alpine3.8

# Add dependencies for Python packages pandas, numpy and pyodbc
RUN apk add --no-cache curl gcc g++ unixodbc-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Project files
ARG PROJECT_DIR=/srv/scripts
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
