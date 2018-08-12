FROM python:3.7-alpine3.7

RUN apk add --no-cache curl gcc g++ unixodbc-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Project Files and Settings
ARG PROJECT_DIR=/var/www/data-quality/api
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["api.py", "0.0.0.0²"]
