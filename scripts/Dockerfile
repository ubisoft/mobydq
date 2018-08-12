
FROM python:3.6.5-alpine3.7

RUN apk add --no-cache --virtual .build-deps g++ libffi-dev && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip install numpy && \
    pip install pandas && \
    pip install cffi && \
    apk del .build-deps

# Install Python and Package Libraries
RUN apk update && apk upgrade && \
  apk add libpq postgresql-dev && \
  apk add build-base && \
  apk add postgresql-libs && \
  apk add python-dev py-pip jpeg-dev zlib-dev unixodbc unixodbc-dev && \
  apk add --no-cache --virtual .build-deps \
  gcc musl-dev \
  build-base postgresql-dev libffi-dev \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" && \
    apk add --virtual .rundeps $runDeps && \
    apk del .build-deps

# Project Files and Settings
ENV LIBRARY_PATH=/lib:/usr/lib
WORKDIR /srv/scripts
COPY requirements.txt ./

#needed to compile numpy
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# disabled for nowRUN pipenv install --system --deploy
# Server
EXPOSE 8000
STOPSIGNAL SIGINT
# ENTRYPOINT ["python"]
# CMD ["hello.py"]
