#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z ${POSTGRES_SERVER} ${POSTGRES_PORT}; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create initial superuser
echo "Creating initial superuser..."
python -c "
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
if not db.query(User).filter(User.email == 'admin@example.com').first():
    user = User(
        email='admin@example.com',
        username='admin',
        hashed_password=get_password_hash('admin123'),
        full_name='Administrator',
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
db.close()
"

echo "Database initialization completed!" 