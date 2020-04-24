FROM node:alpine

# Project files
ARG PROJECT_DIR=/srv/app
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Copy both 'package.json' and 'package-lock.json' (if available)
COPY ./init/package*.json ./

ENV http_proxy=http://proxy.ubisoft.org:3128 https_proxy=http://proxy.ubisoft.org:3128
ENV no_proxy=10.0.0.0/8,192.168.0.0/16,172.16.0.0/12,localhost,127.0.0.1,.ubisoft.org,.ubisoft.onbe,.ubisoft.com
RUN npm config set registry https://artifactory.ubisoft.org/api/npm/npm/

# Install http-server to serve files to Nginx for production
RUN npm install -g http-server

# Install Vue CLI
RUN npm install -g @vue/cli

# Install project dependencies
RUN npm install

# Copy project files and folders to the current working directory
COPY ./entrypoint.sh ./
COPY ./init/ ./

# Use entrypoint to differentiate build process between dev and prod
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]