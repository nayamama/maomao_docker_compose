FROM python:3.7.4

RUN python -m pip install --upgrade pip

RUN apt-get install libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /flask_app \
    && mkdir -p /upload_folder/table_store
#    && mkdir /upload_folder/table_store

WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt 

COPY  . .
RUN chmod +x docker-entrypoint.sh
CMD ["/bin/bash", "docker-entrypoint.sh"]
