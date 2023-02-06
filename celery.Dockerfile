FROM python:3.10-slim

WORKDIR /transport

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements_celery.txt .
RUN pip install --no-cache-dir --upgrade -r requirements_celery.txt

COPY . .
