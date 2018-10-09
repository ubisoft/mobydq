FROM python:3.6.6-alpine3.8

# Project files
ARG PROJECT_DIR=/srv/api
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./init/requirements.txt ./

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./init ./
