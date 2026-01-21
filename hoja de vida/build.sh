#!/usr/bin/env bash

# Exit on error
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

# Navigate to project directory
cd "hoja de vida"

# Install Python dependencies
pip install -r ../requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"