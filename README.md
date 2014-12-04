# PokeAPI


A RESTful API for Pokemon


LICENSE: BSD

http://pokeapi.co


## DEPRECATION

Quite a lot of data is missing from the V1 API.

**As of January 2015, no new data will be added to the v1 API, you will have to use the V2 API instead. This is part of an ongoing deprecation of the v1 API.**

## Setup

1. Download this source code into a working directory.

2. Install the requirements using pip::

    $ make install

This will install all the required packages and libraries for using PokeAPI

3. Set up the local developer environment using the following command::

    $ make setup

4. Run the server using the following command::

    $ make serve

Visit localhost:8000 to see the running website!

If you ever need to wipe the database use this command::

    $ make wipe_db
