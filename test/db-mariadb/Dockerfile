FROM mariadb:latest
# Re-use mysql init as mariadb is practically the same
COPY ./test/db-mysql/init/ /docker-entrypoint-initdb.d/
