FROM mariadb:latest

# Re-use mysql init as mariadb is practically the same
COPY ./init/ /docker-entrypoint-initdb.d/
RUN chown root:root /docker-entrypoint-initdb.d/*.sql