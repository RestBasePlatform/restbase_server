FROM python:3.10-alpine3.13 as builder

COPY requirements.txt requirements.txt

RUN apk update \
  && apk add gcc libc-dev g++ \
  && apk add libffi-dev libxml2 libffi-dev \
  && apk add unixodbc-dev mariadb-dev python3-dev make \
  && python3 -m venv --system-site-packages --without-pip /venv \
  && /venv/bin/python3 -m pip install --no-cache-dir -r requirements.txt \
  && apk del g++ gcc musl-dev libc-dev libffi-dev libxml2 libffi-dev unixodbc-dev mariadb-dev python3-dev \
  && rm requirements.txt \
  && rm /var/cache/apk/*

FROM python:3.10-alpine3.13

COPY --from=builder /venv /venv

WORKDIR /restbase
COPY . /restbase

CMD ["sh", "startup.sh"]
