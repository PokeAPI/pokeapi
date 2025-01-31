FROM python:3.12.8-alpine3.21 AS builder

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN apk add --no-cache postgresql-libs libstdc++
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev \
    postgresql-dev binutils rust cargo && \
    python3 -m pip install -r requirements.txt --no-cache-dir

FROM python:3.12.8-alpine3.21

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE='config.docker-compose'

RUN mkdir /code
WORKDIR /code

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ADD . /code/

RUN addgroup -g 1000 -S pokeapi && \
    adduser -u 1000 -S pokeapi -G pokeapi
USER pokeapi

CMD ["gunicorn", "config.wsgi:application", "-c", "gunicorn.conf.py"]

EXPOSE 80
