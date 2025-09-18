#!/bin/bash

echo "Setting up initial data"

echo "Making migrations"
python manage.py makemigrations --noinput

echo "Migrating"
python manage.py migrate --noinput

echo "Populating database"
python manage.py employee_initial_data
python manage.py location_initial_data

echo "Done"
