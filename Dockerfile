FROM python:3.8-alpine

COPY requirements.txt requirements.txt

RUN apk update \
  && apk add gcc libc-dev g++ \
  && apk add libffi-dev libxml2 libffi-dev \
  && apk add unixodbc-dev mariadb-dev python3-dev \
  && pip3 install -r requirements.txt \
  && apk del g++ gcc musl-dev libc-dev libffi-dev libxml2 libffi-dev unixodbc-dev mariadb-dev python3-dev
  && rm requirements.txt
