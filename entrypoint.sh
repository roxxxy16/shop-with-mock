#!/bin/sh

echo "Waiting for PostgreSQL..."
python - <<END
import os, time, psycopg2
while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "postgres-db"),
            port=int(os.environ.get("POSTGRES_PORT", 5432)),
        )
        conn.close()
        break
    except Exception:
        time.sleep(1)
END
echo "PostgreSQL is up"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:8000 shop.wsgi:application --workers 4
