FROM python:3.11.9-slim

WORKDIR /ghs

RUN pip install --no-cache-dir poetry

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-cache --no-interaction

CMD poetry run python manage.py runserver 0.0.0.0:8000