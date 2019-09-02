#!/bin/sh

flask db init
cp -f migration_env.py migrations/env.py
flask db migrate
flask db upgrade

python create_admin.py 
/usr/local/bin/gunicorn -w 2 --bind 0.0.0.0:8000 wsgi
 
