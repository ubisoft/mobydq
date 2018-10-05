FROM mobydq-scripts:latest

# Install Python dependencies
RUN pip install nose2

# Set Python path to run tests with nose2
ENV PYTHONPATH /srv/scripts:/srv/test:$PYTHONPATH

# Create SQLite database
RUN apt-get install sqlite3

# Test files
WORKDIR /srv
RUN mkdir -p /srv/test && mkdir -p /srv/results
COPY ./db-sqlite ./test/db-sqlite
COPY ./test_db ./test/test_db
COPY ./test_scripts ./test/test_scripts
COPY ./unittest.cfg .

RUN chmod +x test/db-sqlite/database.sh \
    && test/db-sqlite/database.sh