FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=system_zarzadzania_praktykami.settings \
    DEBUG=False

WORKDIR /app

# Systemowe zależności
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Zależności Pythona
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kod projektu
COPY . /app/

# Zbieranie statyk (już z DEBUG=False)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Gunicorn jako serwer WSGI
CMD ["gunicorn", "system_zarzadzania_praktykami.wsgi:application", "--bind", "0.0.0.0:8000"]
