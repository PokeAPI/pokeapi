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

## V2 Database setup

To build out the data you'll need to jump into the Django shell

```
$ python manage.py shell
```
and run the build script with
```
$ execfile('data/v2/build.py')
```
Each time the build script is run it will iterate over each table in the database, wipe it and rewrite each row using the data found in data/v2/csv.
If you don't need all of the data just go into data/v2/build.py and comment out everything but what you need to build the tables you're looking for. This might be useful because some of the csv files are massive (pokemon_moves expecially) and it can take about 30 minutes to build everything.

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
