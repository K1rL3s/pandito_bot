FROM python:3.12.7-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install  --no-cache-dir --upgrade pip setuptools wheel

COPY ./bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /usr/local /usr/local

COPY ./bot ./bot
COPY ./database ./database
CMD ["python", "-m", "bot"]
