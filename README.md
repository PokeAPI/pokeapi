# PokéAPI [![build status](https://img.shields.io/circleci/project/github/PokeAPI/pokeapi/master.svg)](https://circleci.com/gh/PokeAPI/pokeapi) [![License](https://img.shields.io/github/license/PokeAPI/pokeapi.svg)](https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.rst)

[![Backers on Open Collective](https://opencollective.com/pokeapi/backers/badge.svg)](#backers) [![Sponsors on Open Collective](https://opencollective.com/pokeapi/sponsors/badge.svg)](#sponsors)

A RESTful API for Pokémons - [pokeapi.co](http://pokeapi.co)

## Fair use policy

PokéAPI is open and free to use. However, we will ban IP addresses that abuse this privilege. This API is used primarily for educational purposes, and we do not want people inhibiting the education of others. See the fair use guide on the docs for more information. Moreover, we strongly suggest to cache request made, see the [Wrapper section](#official-wrappers) below.

## Join Us On Slack!

Have a question or just want to discuss new ideas and improvements? Hit us up on slack. Consider talking with us here before creating new issue.
This way we can keep issues here a bit more organized and helpful in the long run. Be excellent to each other :smile:

[Sign up easily](https://pokeapi-slack-invite.herokuapp.com/)!

Once you've signed up visit [PokéAPI on Slack](https://pokeapi.slack.com)

## Donations

Help to keep PokéAPI running! If you're using PokéAPI as a teaching resource or for a project, consider sending us a $10 donation to help keep the server up. We get over 2 million requests a month and it's quite costly!

Thank you to all our backers! [Become a backer](https://opencollective.com/pokeapi#backer)

<a href="https://opencollective.com/pokeapi#backers" target="_blank"><img src="https://opencollective.com/pokeapi/backers.svg?width=890"></a>

## Sponsors

Ask your company to also support this open source project by [becoming a sponsor](https://opencollective.com/pokeapi#sponsor).

<a href="https://opencollective.com/pokeapi/sponsor/0/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/1/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/2/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/3/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/4/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/5/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/6/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/7/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/8/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/pokeapi/sponsor/9/website" target="_blank"><img src="https://opencollective.com/pokeapi/sponsor/9/avatar.svg"></a>

## Official Wrappers

* Node server-side [PokeAPI/pokedex-promise-v2](https://github.com/PokeAPI/pokedex-promise-v2) | _Auto caching_
* Browser client-side [PokeAPI/pokeapi-js-wrapper](https://github.com/PokeAPI/pokeapi-js-wrapper) | _Auto caching_
* Java/Kotlin [PokeAPI/pokekotlin](https://github.com/PokeAPI/pokekotlin)
* Python 3 [GregHilmes/pokebase](https://github.com/GregHilmes/pokebase) | _Auto caching_
* Python [PokeAPI/pykemon](https://github.com/PokeAPI/pykemon)
* PHP [lmerotta/phpokeapi](https://github.com/lmerotta/phpokeapi) | _Auto caching, lazy-loading_

## Setup [![pyVersion37](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/download/releases/3.7/)

- Download this source code into a working directory.

- Install the requirements using pip:

```sh
make install
```

This will install all the required packages and libraries for using PokeAPI

- Set up the local developer environment using the following command:

```sh
make setup
```

- Run the server using the following command:

```sh
make serve
```

Visit localhost:8000 to see the running website!

If you ever need to wipe the database use this command:

```sh
make wipe_db
```

## Database setup

Start Django shell

```sh
python manage.py shell --settings=config.local
```

Run the build script with

```py
from data.v2.build import build_all
build_all()
```

Each time the build script is run, it will iterate over each table in the database, wipe it, and rewrite each row using the data found in data/v2/csv.

In informal tests on a Windows PC with a SSD and a 2.50 GHz processor, building against a PostgresQL database took approximately 6 minutes, and building against a SQLite database took about 7.5 minutes or longer, with some varying results.

The option to build individual portions of the database was removed in order to increase performance of the build script.

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
python manage.py migrate --settings=config.docker-compose
```

And then, import the data using the shell

```sh
python manage.py shell --settings=config.docker-compose
```

You can use the `build_all()` method, or individuals data building functions (See _V2 Database setup_)

```py
from data.v2.build import build_all
build_all()
```

Browse [localhost/api/v2/](http://localhost/api/v2/) or [localhost/api/v2/pokemon/bulbasaur/](http://localhost/api/v2/pokemon/bulbasaur/)

For the moment, this setup doesn't allow you to use the `scale` command.

## Docker (obsolete)

The application can be built and run as a Docker container for easy deployments

From the root directory of the cloned repo

```sh
docker build -t pokeapi .
```

Run the container on host port 8000

```sh
docker run -d -p 8000:8000 pokeapi
```

## Contributing

This project exists thanks to all the people who contribute. [[Contribute]](blob/master/CONTRIBUTING.md).
<a href="graphs/contributors"><img src="https://opencollective.com/pokeapi/contributors.svg?width=890" /></a>

All contributions are welcome: bug fixes, data contributions, recommendations.

Please see the [issues on GitHub](https://github.com/PokeAPI/pokeapi/issues) before you submit a pull request or raise an issue, someone else might have beat you to it.

To contribute to this repository:

- [Fork the project to your own GitHub profile](https://help.github.com/articles/fork-a-repo/)

- Download the project using git clone:

    ```sh
    git clone git@github.com:<YOUR_USERNAME>/pokeapi.git
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

## DEPRECATION

As of October 2018, the v1 API has been removed from PokéAPI. For more information, see [pokeapi.co/docs/v1.html](https://pokeapi.co/docs/v1.html).