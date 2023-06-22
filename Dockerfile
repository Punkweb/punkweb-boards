FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /webapps
WORKDIR /webapps

# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y

RUN pip install -U pip setuptools

COPY requirements.txt /webapps/

RUN pip install -r /webapps/requirements.txt

ADD . /webapps/

# Django service
EXPOSE 8000
