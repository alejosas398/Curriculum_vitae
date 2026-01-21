#!/bin/bash
set -o errexit

# Determinar el directorio base
if [ -d "hoja de vida" ]; then
    cd "hoja de vida"
    REQ_PATH="../requirements.txt"
else
    REQ_PATH="requirements.txt"
fi

# Install Python dependencies
pip install -r $REQ_PATH

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"
