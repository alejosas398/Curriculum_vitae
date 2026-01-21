#!/usr/bin/env bash
# exit on error
set -o errexit

pip install wheel
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata initial_data.json
gunicorn hoja_de_vida.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver