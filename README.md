<br/>

<div align="center">
	<img height="200" src="https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi.svg?sanitize=true" alt="PokeAPI">

[![build status](https://img.shields.io/circleci/project/github/PokeAPI/pokeapi/master.svg)](https://circleci.com/gh/PokeAPI/pokeapi)
[![data status](https://img.shields.io/circleci/build/github/PokeAPI/api-data?label=data)](https://github.com/PokeAPI/api-data)
[![deploy status](https://img.shields.io/circleci/build/github/PokeAPI/deploy?label=deploy)](https://github.com/PokeAPI/deploy)
[![License](https://img.shields.io/github/license/PokeAPI/pokeapi.svg)](https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md)
[![Backers on Open Collective](https://opencollective.com/pokeapi/backers/badge.svg)](https://opencollective.com/pokeapi)
[![Sponsors on Open Collective](https://opencollective.com/pokeapi/sponsors/badge.svg)](https://opencollective.com/pokeapi)

<br/>

</div>

<br/>

A RESTful API for Pokémon - [pokeapi.co](https://pokeapi.co)

## Join Us On Slack!

Have a question or just want to discuss new ideas and improvements? Hit us up on slack. Consider talking with us here before creating new issue.
This way we can keep issues here a bit more organized and helpful in the long run. Be excellent to each other :smile:

[Sign up](https://pokeapi-slack-invite.herokuapp.com/) easily!

Once you've signed up visit [PokéAPI on Slack](https://pokeapi.slack.com)

## Official Wrappers

* Node server-side [PokeAPI/pokedex-promise-v2](https://github.com/PokeAPI/pokedex-promise-v2) | _Auto caching_
* Browser client-side [PokeAPI/pokeapi-js-wrapper](https://github.com/PokeAPI/pokeapi-js-wrapper) | _Auto caching_
* Java/Kotlin [PokeAPI/pokekotlin](https://github.com/PokeAPI/pokekotlin)
* Python 3 [GregHilmes/pokebase](https://github.com/GregHilmes/pokebase) | _Auto caching_
* Python 2/3 [PokeAPI/pokepy](https://github.com/PokeAPI/pokepy) | _Auto caching_
* PHP [lmerotta/phpokeapi](https://github.com/lmerotta/phpokeapi) | _Auto caching, lazy loading_
* Ruby [rdavid1099/poke-api-v2](https://github.com/rdavid1099/poke-api-v2)
* .Net Standard [mtrdp642/PokeApiNet](https://github.com/mtrdp642/PokeApiNet) | _Auto caching_
* Go [mtslzr/pokeapi-go](https://github.com/mtslzr/pokeapi-go) | _Auto caching_
* Dart [prathanbomb/pokedart](https://github.com/prathanbomb/pokedart)
* Rust [lunik1/pokerust](https://gitlab.com/lunik1/pokerust) | _Auto caching_
* Spring Boot [dlfigueira/spring-pokeapi](https://github.com/dlfigueira/spring-pokeapi) | _Auto caching_
* Swift [kinkofer/PokemonAPI](https://github.com/kinkofer/PokemonAPI)

## Setup [![pyVersion37](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/download/releases/3.7/)

- Download this source code into a working directory, be sure to use the flag `--recurse-submodules` to clone also our submodules.

- Install the requirements using pip:

    ```sh
    make install
    # This will install all the required packages and libraries for using PokeAPI
    ```

- Set up the local development environment using the following command:

    ```sh
    make setup
    ```

- Run the server using the following command:

    ```sh
    make serve
    ```

## Database setup

Start the Django shell by

```sh
python manage.py shell --settings=config.local
```

Run the build script with

```py
from data.v2.build import build_all
build_all()
```

Visit [localhost:8000/api/v2/](localhost:8000/api/v2/) to see the running API!

Each time the build script is run, it will iterate over each table in the database, wipe it, and rewrite each row using the data found in data/v2/csv.

In informal tests on a Windows PC with a SSD and a 2.50 GHz processor, building against a PostgresQL database took approximately 6 minutes, and building against a SQLite database took about 7.5 minutes or longer, with some varying results.

The option to build individual portions of the database was removed in order to increase performance of the build script.

If you ever need to wipe the database use this command:

```sh
make wipe_db
```

## Docker Compose

There is also a multi-container setup, managed by [Docker Compose](https://docs.docker.com/compose/). This setup allow you to deploy a production-like environment, with separate containers for each services.

Start the process using

```sh
docker-compose up --build
```

You can specify the `-d` switch to start in detached mode.
This will bind port 80 and 443. Unfortunately, unlike the `docker` command, there is no command line arguments to specify ports. If you want to change them, edit the `docker-compose.yml` file.

After that, start the migration process

```sh
docker-compose exec app python manage.py migrate --settings=config.docker-compose
```

And then, import the data using the shell

```sh
docker-compose exec app python manage.py shell --settings=config.docker-compose
```

Then use the `build_all()` method in the shell to populate the database.

```py
from data.v2.build import build_all
build_all()
```

Browse [localhost/api/v2/](http://localhost/api/v2/) or [localhost/api/v2/pokemon/bulbasaur/](http://localhost/api/v2/pokemon/bulbasaur/)

This setup doesn't allow you to use the `scale` command.

## Donations

Help to keep PokéAPI running! If you're using PokéAPI as a teaching resource or for a project, consider sending us a $10 donation to help keep the service up. We get almost 20 million requests a month!

Thank you to all our backers! [Become a backer](https://opencollective.com/pokeapi#backer)

<a href="https://opencollective.com/pokeapi#backers" target="_blank"><img src="https://opencollective.com/pokeapi/backers.svg?width=890"></a>

## Contributing

This project exists thanks to all the people who [contribute](https://github.com/PokeAPI/pokeapi/blob/master/CONTRIBUTING.md)

<a href="graphs/contributors"><img src="https://opencollective.com/pokeapi/contributors.svg?width=890" /></a>

All contributions are welcome: bug fixes, data contributions, recommendations.

Please see the [issues on GitHub](https://github.com/PokeAPI/pokeapi/issues) before you submit a pull request or raise an issue, someone else might have beat you to it.

To contribute to this repository:

- [Fork the project to your own GitHub profile](https://help.github.com/articles/fork-a-repo/)

- Download the forked project using git clone:

    ```sh
    git clone --recurse-submodules git@github.com:<YOUR_USERNAME>/pokeapi.git
    ```

- Create a new branch with a descriptive name:

    ```sh
    git checkout -b my_new_branch
    ```

- Write some code, fix something, and add a test to prove that it works. *No pull request will be accepted without tests passing, or without new tests if new features are added.*

- Commit your code and push it to GitHub

- [Open a new pull request](https://help.github.com/articles/creating-a-pull-request/) and describe the changes you have made.

- We'll accept your changes after review.

Simple!

## Deprecation

As of October 2018, the v1 API has been removed from PokéAPI. For more information, see [pokeapi.co/docs/v1.html](https://pokeapi.co/docs/v1.html).
