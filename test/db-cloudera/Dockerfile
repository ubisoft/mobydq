FROM cloudera/quickstart:latest

# Project files
ARG PROJECT_DIR=/srv/db-cloudera
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./init/ ./

# Grant permissions for scripts to be executable
RUN chmod +x $PROJECT_DIR/entrypoint.sh

CMD ["/bin/bash", "entrypoint.sh"]
