FROM mobydq-scripts:latest

# Install Python dependencies
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Set Python path to run tests with nose2
ENV PYTHONPATH /srv/scripts:$PYTHONPATH
ENV PYTHONPATH /srv/srv/test:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_db:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_api:$PYTHONPATH
ENV PYTHONPATH /srv/test/test_scripts:$PYTHONPATH


# Create SQLite database
RUN apt-get install -y sqlite3

# Test files
WORKDIR /srv
RUN mkdir -p /srv/test
COPY ./db-sqlite ./test/db-sqlite
COPY ./test_db ./test/test_db
COPY ./test_api ./test/test_api
COPY ./test_scripts ./test/test_scripts
COPY ./unittest.cfg .

RUN chmod +x test/db-sqlite/database.sh \
    && test/db-sqlite/database.sh

COPY .pylintrc ./
