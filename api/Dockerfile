FROM python:3.6.6-alpine3.8

# Project files
ARG PROJECT_DIR=/srv/api
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./init ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
