FROM python:3.10.16-bookworm

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'
WORKDIR /code

ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/

RUN groupadd -g 1000 pokeapi && \
    useradd -u 1000 -g pokeapi pokeapi

USER pokeapi
CMD gunicorn config.wsgi:application -c gunicorn.conf.py