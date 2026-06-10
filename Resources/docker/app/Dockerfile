FROM python:3.14-alpine as builder

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PROJECT_ENVIRONMENT=/code/.venv

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

FROM python:3.14-alpine
# git is a dependency for the meta endpoint
RUN apk add --no-cache git

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE='config.docker-compose'
ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code

RUN addgroup -g 1000 -S pokeapi && \
    adduser -u 1000 -S pokeapi -G pokeapi

COPY --chown=pokeapi:pokeapi . /code/

COPY --from=builder --chown=pokeapi:pokeapi /code/.venv /code/.venv

USER pokeapi

EXPOSE 80

CMD ["gunicorn", "config.wsgi:application", "-c", "gunicorn.conf.py"]
