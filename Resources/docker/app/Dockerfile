FROM python:3.13.7-alpine AS builder

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

# Install UV
RUN apk add --no-cache curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH for this stage
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
ADD pyproject.toml uv.lock* /code/

# Install dependencies
RUN apk add --no-cache postgresql-libs libstdc++
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev \
    postgresql-dev binutils rust cargo && \
    uv sync --frozen

FROM python:3.13.7-alpine

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE='config.docker-compose'

RUN mkdir /code
WORKDIR /code

# Copy UV and virtual environment from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /code/.venv /code/.venv

# Add UV to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install runtime dependencies
RUN apk add --no-cache postgresql-libs libstdc++

# Copy application code
ADD . /code/

RUN addgroup -g 1000 -S pokeapi && \
    adduser -u 1000 -S pokeapi -G pokeapi
USER pokeapi

CMD ["uv", "run", "gunicorn", "config.wsgi:application", "-c", "gunicorn.conf.py"]

EXPOSE 80
