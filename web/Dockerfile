FROM python:2

RUN python -m pip install --upgrade pip

RUN apt-get install libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /flask_app

ENV FLASK_CONFIG=development
WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt 

COPY  . .
RUN chmod +x docker-entrypoint.sh
CMD ["/bin/bash", "docker-entrypoint.sh"]
