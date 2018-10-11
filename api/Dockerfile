FROM python:3.6.6-alpine3.8

# Project files
ARG PROJECT_DIR=/srv/api
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Install Python dependencies
COPY ./init/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./init ./
