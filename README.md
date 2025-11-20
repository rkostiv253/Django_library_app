# Django_library_app

This is an API for library service built with Python using Django Rest Framework. This app allows to add authors, 
genres, books and borrow and return books from library.

## Installation 

Python3 must be already installed
```shell
git clone https://github.com/rkostiv253/Django_library_app.git
cd Django_library_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set SECRET_KEY=<your secret key>
python3 manage.py makemigrations
python3 manage.py migrate
```

## Features

- JWT Authenticated
- Admin panel /admin/
- Documentation is located in api/doc/swagger
- Add authors, genres and books
- Borrow books and return them

## Tech stack

- **Backend**: Python, Django Rest Framework
- **Database**: SQLite

├── borrowing
│   └──  tests
│        └── __init__.py
│        └── test_borrowing_api.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── library
│   └──  tests
│        └── __init__.py
│        └── test_library_api.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── library_service
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .dockerignore
├── .env.sample
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── .flake8
├── manage.py
├── README.md
├── requirements.txt
