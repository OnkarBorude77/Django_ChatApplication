FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y build-essential libpq-dev gcc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=chatapp.settings
RUN python manage.py collectstatic --noinput

EXPOSE 8080
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "chatapp.asgi:application"]
