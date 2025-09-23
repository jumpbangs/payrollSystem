# Makefile

.PHONY: run migrate shell test

run:
	source backend_env/bin/activate && python manage.py runserver

migrate:
	python manage.py makemigrations && python manage.py migrate

shell:
	python manage.py shell

test:
	python manage.py test
