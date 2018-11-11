FROM mobydq-scripts:latest

WORKDIR /srv
RUN mkdir -p /srv/test
RUN mkdir -p /srv/api

# Install Python dependencies
COPY ./api/init/requirements.txt ./api
COPY ./test/requirements.txt ./test

RUN pip install -r ./api/requirements.txt
RUN pip install -r ./test/requirements.txt

# Set Python path to run tests with nose2
ENV PYTHONPATH /srv/scripts:$PYTHONPATH
ENV PYTHONPATH /srv/test:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_db:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_api:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_scripts:$PYTHONPATH

# Create SQLite database
RUN apt-get install -y sqlite3

# Test files
COPY ./api/init ./api
COPY ./test/db-sqlite ./test/db-sqlite
COPY ./test/test_db ./test/test_db
COPY ./test/test_api ./test/test_api
COPY ./test/test_scripts ./test/test_scripts
COPY ./test/shared ./test/shared
COPY ./test/unittest.cfg .
COPY ./test/pylintrc .

RUN chmod +x test/db-sqlite/database.sh \
    && test/db-sqlite/database.sh
