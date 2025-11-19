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
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
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

# Django_library_app
# Django_library_app
