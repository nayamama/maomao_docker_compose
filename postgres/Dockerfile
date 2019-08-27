FROM postgres:latest

USER postgres
COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
#WORKDIR /fixtures
#RUN /fixtures/setup.sh