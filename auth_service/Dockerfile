FROM python:3.11.9-alpine

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

ENV POETRY_VIRTUALENVS_CREATE=false

EXPOSE 8080