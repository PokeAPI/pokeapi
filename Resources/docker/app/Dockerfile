FROM python:3.10.16-bookworm

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/

RUN addgroup -g 1000 -S pokeapi && \
    adduser -u 1000 -S pokeapi -G pokeapi

USER pokeapi
CMD gunicorn config.wsgi:application -c gunicorn.conf.py
EXPOSE 80
