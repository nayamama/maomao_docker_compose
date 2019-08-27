FROM postgres:latest

USER postgres
COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
CMD psql -f /docker-entrypoint-initdb.d/10-init.sql
