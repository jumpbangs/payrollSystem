#!/bin/bash

echo "Setting up initial data"

echo "Making migrations"
python manage.py makemigrations --noinput

echo "Migrating"
python manage.py migrate --noinput

echo "Popluating database"
python manage.py employee_inital_data
python manage.py location_inital_data

echo "Done"
