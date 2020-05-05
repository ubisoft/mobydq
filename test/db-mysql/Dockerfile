FROM mysql:latest
COPY ./init/ /docker-entrypoint-initdb.d/
RUN chown root:root /docker-entrypoint-initdb.d/*.sql