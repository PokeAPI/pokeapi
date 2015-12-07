# PokeAPI


A RESTful API for Pokemon


LICENSE: BSD

http://pokeapi.co


## DEPRECATION

Quite a lot of data is missing from the V1 API.

**As of January 2015, no new data will be added to the v1 API, you will have to use the V2 API instead. This is part of an ongoing deprecation of the v1 API.**

See [This blog post for more information](http://phalt.co/if-you-have-data-they-will-consume-it).

## Setup

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


## Contributing

All contributions are welcome: bug fixes, data contributions, recommendations.

Please see the [issues on GitHub](https://github.com/phalt/pokeapi/issues) before you submit a pull request or raise an issue, someone else might have beat you to it.

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
