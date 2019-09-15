#!/bin/sh

set -x

# enable postgresSQL Apt repo
apt-get update && apt-get -y install sudo
# sudo apt-get install wget ca-certificates
# wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# install postgresql
# sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
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
 
