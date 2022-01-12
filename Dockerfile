# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP="__init__.py"
ENV FLASK_ENV="Development"

CMD [ "python3", "-m" , "flask", "run", "--host=localhost", "-p", "8080"]