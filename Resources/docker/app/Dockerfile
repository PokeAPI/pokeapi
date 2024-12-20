FROM python:3.10.14-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN apk add --no-cache postgresql-libs libstdc++
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev \
    postgresql-dev rust cargo && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
ADD . /code/

RUN addgroup -g 1000 -S pokeapi && \
    adduser -u 1000 -S pokeapi -G pokeapi

USER pokeapi
CMD gunicorn config.wsgi:application -c gunicorn.conf.py
EXPOSE 80
