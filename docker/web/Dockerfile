#FROM python:3.4-alpine
FROM ubuntu:18.04
RUN mkdir /code
WORKDIR /code
RUN apt update
RUN apt install -y mongodb-clients
RUN apt install -y python3-minimal
RUN apt install -y python3-pip
RUN pip3 install flask
RUN pip3 install pymongo
