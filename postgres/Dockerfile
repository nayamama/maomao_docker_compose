FROM postgres:latest

USER postgres
COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
CMD /etc/init.d/postgresql start && psql -f /docker-entrypoint-initdb.d/10-init.sql && /etc/init.d/postgresql stop
