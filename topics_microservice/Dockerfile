FROM python:3.12.4-slim

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install --no-root

EXPOSE 8080
