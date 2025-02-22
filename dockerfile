FROM python:3.11.4-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN mkdir -p /app
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --upgrade --ignore-installed pip setuptools

ADD requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

ADD . /app
