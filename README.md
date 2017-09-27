# PokeAPI

A RESTful API for Pokémon

LICENSE: [BSD](https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.rst)

http://pokeapi.co

[![Backers on Open Collective](https://opencollective.com/pokeapi/backers/badge.svg)](#backers) [![Sponsors on Open Collective](https://opencollective.com/pokeapi/sponsors/badge.svg)](#sponsors) [![ghit.me](https://ghit.me/badge.svg?repo=PokeAPI/pokeapi)](https://ghit.me/repo/PokeAPI/pokeapi)

## Fair use policy

PokéAPI is open and free to use. However, we will ban IP addresses that abuse this privilege. This API is used primarily for educational purposes, and we do not want people inhibiting the education of others. See the fair use guide on the docs for more information.

## Join Us On Slack!
Have a question or just want to discuss new ideas and improvements? Hit us up on slack. Consider talking with us here before creating new issue.
This way we can keep issues here a bit more organized and helpful in the long run. Be excellent to eachother :)

[Sign up easily](https://pokeapi-slack-invite.herokuapp.com/)!

Once you've signed up visit [PokeAPI on Slack](https://pokeapi.slack.com)

## Donations

Help to keep PokéAPI running! If you're using PokéAPI as a teaching resource or for a project, consider sending us a $10 donation to help keep the server up. We get over 2 million requests a month and it's quite costly!

Thank you to all our backers! [[Become a backer](https://opencollective.com/pokeapi#backer)]

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





## DEPRECATION

Quite a lot of data is missing from the V1 API.

**As of January 2015, no new data will be added to the v1 API, you will have to use the V2 API instead.**

See [This blog post for more information](http://phalt.co/if-you-have-data-they-will-consume-it).

## Setup [![pyVersion27](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/) 

- Download this source code into a working directory.

- Install the requirements using pip:
```
$ make install
```
This will install all the required packages and libraries for using PokeAPI

- Set up the local developer environment using the following command:
```
$ make setup
```
- Run the server using the following command::
```
$ make serve
```
Visit localhost:8000 to see the running website!

If you ever need to wipe the database use this command:
```
$ make wipe_db
```

## V1 Database setup

Start Django shell
```
$ python manage.py shell --settings=config.local
```
import build functions
```
$ from data.v1.build import *
```
run the functions in order to populate v1 tables
```
$ build_pokes()
$ build_abilities()
$ build moves()
etc...
```


## V2 Database setup

Start Django shell
```
$ python manage.py shell --settings=config.local
```

run the build script with
```
$ from data.v2.build import build_all
$ build_all()
```
Each time the build script is run it will iterate over each table in the database, wipe it and rewrite each row using the data found in data/v2/csv.
When building against sqlite we've heard it can take a ridiculously long time to finish building out the database. In this case you can set up just the portions of the db that you need.
```
$ from data.v2.build import *
$ build_languages()
$ build_abilities()
...
```

Heres a list of the data building functions
- build_languages()
- build_regions()
- build_generations()
- build_versions()
- build_stats()
- build_damage_classes()
- build_abilities()
- build_characteristics()
- build_egg_groups()
- build_growth_rates()
- build_items()
- build_types()
- build_contests()
- build_moves()
- build_berries()
- build_natures()
- build_genders()
- build_experiences()
- build_machines()
- build_evolutions()
- build_pokedexes()
- build_locations()
- build_pokemons()
- build_encounters()
- build_pal_parks()


## Docker

The application can be built and run as a Docker container for easy deployments

From the root directory of the cloned repo
```
docker build -t pokeapi .
```

Run the container on host port 8000
```
docker run -d -p 8000:8000 pokeapi
```


## Docker Compose

There is also a multi-container setup, managed by [Docker Compose](https://docs.docker.com/compose/). This setup allow you to deploy a production-like environment, with separate containers for each services.

Create data volumes for Redis and Postgres
```
docker volume create --name=redis_data
docker volume create --name=pg_data
```

Start the process using
```
docker-compose up
```
You can specify the ```-d``` switch to start in detached mode.   
This will bind port 80 and 443. Unfortunately, unlike the ```docker``` command, there is no command line arguments to specify ports. If you want to change them, edit the ```docker-compose.yml``` file.

After that, start the migration process
```
docker-compose exec app python manage.py migrate
```

And then, import the data using the shell
```
docker-compose exec app python manage.py shell
```

You can use the ```build_all()``` method, or individuals data building functions (See _V2 Database setup_)
```
from data.v2.build import build_all
build_all()
```

For the moment, this setup doesn't allow you to use the ```scale``` command.

## Contributing

This project exists thanks to all the people who contribute. [[Contribute]](blob/master/CONTRIBUTING.md).
<a href="graphs/contributors"><img src="https://opencollective.com/pokeapi/contributors.svg?width=890" /></a>

All contributions are welcome: bug fixes, data contributions, recommendations.

Please see the [issues on GitHub](https://github.com/PokeAPI/pokeapi/issues) before you submit a pull request or raise an issue, someone else might have beat you to it.

To contribute to this repository:

- [Fork the project to your own GitHub profile](https://help.github.com/articles/fork-a-repo/)

- Download the project using git clone:
```
git clone git@github.com:<YOUR_USERNAME>/pokeapi.git
```
- Create a new branch with a descriptive name:
```
git checkout -b my_new_branch
```
- Write some code, fix something, and add a test to prove that it works. **No pull request will be accepted without tests passing, or without new tests if new features are added.**

- Commit your code and push it to GitHub

- [Open a new pull request](https://help.github.com/articles/creating-a-pull-request/) and describe the changes you have made.

- We'll accept your changes after review.

Simple!
