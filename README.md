# Payroll System (Django-rest-framework)

A simple payroll system to showcase the use of [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/).

## Create virtual environment, update pip and select the given virtual environment

```bash
$ python3 -m venv backend_env
$ pip install --upgrade pip
$ source backend_env/bin/activate
```

## Installation the required packages

```bash
$ pip install -r requirements.txt
```

## Populate the database with stock data
```bash
$ ./script/inital_setup.sh
```

## Usage

```bash
$ python manage.py runserver
```

## Create/Update requirements.txt

```bash
$ pip freeze > requirements.txt
```

##
