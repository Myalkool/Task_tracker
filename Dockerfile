FROM python:3.11-slim

# Установка зависимостей и bash
RUN apt-get update && apt-get install -y \
    bash build-essential libpq-dev gcc \
    && apt-get clean

# Установка зависимостей Python
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .
