FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -qy --no-install-recommends python3 python3-pip python3-setuptools

RUN mkdir /app
RUN useradd -d /app app

ADD requirements.txt /app
RUN pip3 install -r /app/requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_APP "webapp:launch()"

USER app
WORKDIR /app
