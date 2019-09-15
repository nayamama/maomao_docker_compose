FROM python:3

RUN python -m pip install --upgrade pip

RUN apt-get install libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /flask_app \
    && mkdir /upload_folder

ENV FLASK_CONFIG=development
WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt 

COPY  . .
RUN chmod +x docker-entrypoint.sh
CMD ["/bin/bash", "docker-entrypoint.sh"]
