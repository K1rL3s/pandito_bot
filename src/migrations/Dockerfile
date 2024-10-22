FROM python:3.12.7-slim-bullseye AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./src/run/requirements.txt .

RUN pip install  --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.12.7-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY ./alembic.ini ./alembic.ini
COPY ./src/migrations ./src/migrations
COPY ./src/infrastructure/database ./src/infrastructure/database

CMD ["alembic", "upgrade", "head"]