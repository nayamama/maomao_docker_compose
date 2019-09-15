FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
CMD /etc/init.d/postgresql start \ 
   && sleep 5 \
   && psql -h localhost -U postgres -f /docker-entrypoint-initdb.d/10-init.sql \
   && psql -h localhost -U postgres -d stage_db -c "delete from alembic_version;" \
   && /etc/init.d/postgresql stop

