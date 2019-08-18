#!/bin/bash

docker-compose build
docker-compose up -d

docker-compose run postgres psql -h postgres_host -U postgres -c 'create database stage_db'
docker-compose run postgres psql -h postgres_host -U postgres -c 'create user stage_test with password '1234abcd'
docker-compose run postgres psql -h postgres_host -U postgres -c 'grant all privileges on database stage_db to stage_test'

