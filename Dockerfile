FROM python:3.12-slim

# Ustawienia środowiska Pythona
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Katalog roboczy
WORKDIR /app

# Systemowe zależności (np. dla psycopg2, Pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Pythona
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopia kodu projektu
COPY . /app/

COPY . .
ENV DJANGO_SETTINGS_MODULE=python.settings
RUN python manage.py migrate
RUN python manage.py init_roles
RUN python manage.py seed_app_praktyki

# Port dla runserver
EXPOSE 8000

# Komenda startowa (dev)a
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
