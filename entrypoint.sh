#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py tailwind build
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:6942