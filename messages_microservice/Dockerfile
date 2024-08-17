FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY .. .

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["poetry", "run", "python", "src/app.py"]
