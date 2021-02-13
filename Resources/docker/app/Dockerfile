FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'
ENV PYTHONHASHSEED 'random'

RUN mkdir /code
WORKDIR /code
VOLUME /code

ADD requirements.txt /code/
RUN \
    apk add --no-cache postgresql-libs libstdc++ && \
    apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
ADD . /code/

CMD gunicorn config.wsgi:application -c gunicorn.py.ini
EXPOSE 8000
