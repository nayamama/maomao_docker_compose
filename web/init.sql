-- Create a new database called ''
-- Connect to the 'master' database to run this snippet

CREATE DATABASE stage_db;
create user stage_test with password '1234abcd';

grant all privileges on database stage_db to stage_test;
