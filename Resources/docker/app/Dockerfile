FROM python:3.10.16-bookworm AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apt-get install rustc cargo
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.16-bookworm

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.docker-compose'
WORKDIR /code

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ADD . /code/

RUN groupadd -g 1000 pokeapi && \
    useradd -u 1000 -g pokeapi pokeapi

USER pokeapi
CMD gunicorn config.wsgi:application -c gunicorn.conf.py