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

## Endpoints
Endpoints and the REST API that is used in the following project.

---
## Employee
### Auth Views
- Login (POST)
- Logout (DELETE)
- Change Password (POST)

### Employee Views
- GET
- POST
- PATCH
- DELETE

### Employment Terms View
- GET
- PATCH

### Payment View
- GET
- POST
- PATCH
- DELETE

---
## Locations
### Address View
- GET
- POST
- PUT
- DELETE

### City View
- GET
- POST
- PUT
- DELETE

### Country View
- GET
- POST
- PUT

---
## Worklogs
### Client View
- GET
- POST
- PATCH
- DELETE

### Worklog View
- GET
- POST
- PATCH
- DELETE

### Job View
- GET
- POST
- PATCH
- DELETE
