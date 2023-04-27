# Quick reference

- **Maintained by**:
    [the PokeAPI Contributors](https://github.com/PokeAPI/pokeapi/graphs/contributors)

- **Where to get help**:
    [PokeAPI Slack](http://pokeapi.slack.com/).

- **Where to file issues**:
    [https://github.com/PokeAPI/pokeapi/issues](https://github.com/PokeAPI/pokeapi/issues)

- **Source of this description**:
    [pokeapi repo's `Resources/docker/app/` directory](https://github.com/PokeAPI/pokeapi/blob/master/Resources/docker/app/README.md)

## Supported tags and respective `Dockerfile` links

- [`master`](https://github.com/PokeAPI/pokeapi/blob/master/Resources/docker/app/Dockerfile)
- [`staging`](https://github.com/PokeAPI/pokeapi/blob/staging/Resources/docker/app/Dockerfile)

> `pokeapi` uses `python:3.10-alpine` as base image.

## What is PokeAPI?

PokeAPI is a full RESTful API linked to an extensive database detailing everything about the Pokémon main game series.

> [pokeapi.co](https://pokeapi.co/)

![logo](https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png)

## How to use this image

This container connects to a Postgres database via the environment variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.

The container connects to a Redis cache via the environment variable `REDIS_CONNECTION_STRING`.

### Run the container

The container exposes port `80`. It needs a PostgreSQL and a Redis instance to connect to. Refer to the section [How to use this image](./how-to-use-this-image) for mapping the environment variables.

It's recommended to use the provided [docker-compose.yml](https://github.com/PokeAPI/pokeapi/blob/master/docker-compose.yml) to start a container from this image.

### Build the data

Pokémon data isn't automatically present in this image. All Pokémon data is persisted in a PostgreSQL database and thus needs to be built.

When the container is up and running, run the following shell commands:

```sh
docker exec pokeapi python manage.py migrate --settings=config.docker-compose
docker exec pokeapi sh -c 'echo "from data.v2.build import build_all; build_all()" | python manage.py shell --settings=config.docker-compose'
```
