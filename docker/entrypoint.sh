#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL to be ready at $DB_HOST:$DB_PORT..."

    until pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; do
      echo "Waiting for PostgreSQL..."
      sleep 0.5
    done

    # Optional: sleep 1s more to allow full recovery
    sleep 1

    echo "PostgreSQL started"
fi

# Apply database migrations
python backend/manage.py migrate

# Create superuser if needed
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python backend/manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

exec "$@"
