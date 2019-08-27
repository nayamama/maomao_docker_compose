FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
CMD /etc/init.d/postgresql start \ 
   && sleep 5 \
   && psql -U postgres -f /docker-entrypoint-initdb.d/10-init.sql \
   && /etc/init.d/postgresql stop

