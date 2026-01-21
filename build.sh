#!/bin/bash
set -o errexit

# Install system dependencies for WeasyPrint
apt-get update
apt-get install -y \
  libcairo2 \
  libcairo2-dev \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info \
  libharfbuzz0b \
  libpangoft2-1.0-0

# Determinar el directorio base
if [ -d "hoja de vida" ]; then
    cd "hoja de vida"
    REQ_PATH="../requirements.txt"
else
    REQ_PATH="requirements.txt"
fi

pip install -r $REQ_PATH

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"
