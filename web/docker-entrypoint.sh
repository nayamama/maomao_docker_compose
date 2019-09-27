#!/bin/sh

set -x

# enable postgresSQL Apt repo
apt-get update && apt-get -y install sudo
sudo apt-get install -y postgresql-client

# initiate db
sleep 5 
psql -h postgres_host -U postgres -f init.sql 
psql -h postgres_host -U postgres -d stage_db -c "delete from alembic_version;" 

# initiate flask db and migrate db
flask db init
cp -f migration_env.py migrations/env.py
flask db migrate
flask db upgrade

python create_admin.py 
/usr/local/bin/gunicorn -w 2 --bind 0.0.0.0:8000 wsgi
 
