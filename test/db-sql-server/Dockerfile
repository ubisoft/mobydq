FROM microsoft/mssql-server-linux:latest

# Project files
ARG PROJECT_DIR=/srv/db-sql-server
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY ./db-sql-server/init/ ./

# Grant permissions for scripts to be executable
RUN chmod +x $PROJECT_DIR/entrypoint.sh
RUN chmod +x $PROJECT_DIR/setup.sh
