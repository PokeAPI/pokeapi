ARG PYTHON_VERSION=3.12-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE='config.docker-compose'

RUN mkdir /code
WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    rustc \
    cargo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 1001 --system pokeapi && \
    adduser --uid 1001 --system --ingroup pokeapi --shell /bin/bash pokeapi

RUN chown -R pokeapi:pokeapi /code

USER pokeapi

ADD requirements.txt /code/
ADD test-requirements.txt /code/
RUN python3 -m pip install -r test-requirements.txt --no-cache-dir

ADD . /code/

CMD ["sleep", "infinity"]