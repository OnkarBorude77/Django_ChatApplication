# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 10000

# Run Daphne ASGI server (do NOT run collectstatic here)
CMD python manage.py migrate && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p 10000 chatapp.asgi:application
 