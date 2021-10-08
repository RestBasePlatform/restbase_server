FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN apt update -y \
  && apt install -y --no-install-recommends gcc libc-dev g++ make \
  && apt install -y --no-install-recommends libffi-dev libxml2 libffi-dev \
  && apt install -y --no-install-recommends unixodbc-dev python3-dev \
  && pip3 install -r requirements.txt \
  && rm requirements.txt \
  && apt-get remove -y gcc libc-dev g++ make libffi-dev libxml2 libffi-dev unixodbc-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /restbase
COPY . /restbase

CMD ["sh", "startup.sh"]
