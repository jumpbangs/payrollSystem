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
### Auth Views ✅ - Has schema
- Login (POST)
- Logout (DELETE)
- Change Password (POST)

### Employee Views ✅ - Has schema
- GET
- POST
- PATCH
- DELETE

### Employment Terms View ✅ - Has schema
- GET
- PATCH

### Payment View ✅ - Has schema
- GET
- POST
- PATCH
- DELETE

### Employee Banking Detail View
- GET
- POST
- PATCH

### Team View
- GET
- POST
- PATCH
- DELETE

---
## Locations
### Address View ✅ - Has schema
- GET
- POST
- PUT
- DELETE

### City View ✅ - Has schema
- GET
- POST
- PUT
- DELETE

### Country View ✅ - Has schema
- GET
- POST
- PUT

---
## Worklogs
### Client View ✅ - Has schema
- GET
- POST
- PATCH

### Worklog View ✅ - Has schema
- GET
- POST
- PATCH
- DELETE

### Job View
- GET
- POST
- PATCH
- DELETE

---

### Python pyproject config

"F" - Pyflakes rules
"T" - flake8 TODO comments rules
"UP" - Warn if certain things can changed due to newer Python versions
"I" - Sort imports properly,
"ICN" - flake8 import conventions
"COM" - enforce trailing comma rules
"FBT" - detect boolean traps
