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

> Beta GraphQL support is rolling out! Check out the [GraphQL paragraph](#graphql--) for more info.

## Setup &nbsp; [![pyVersion310](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/download/releases/3.10/)

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

### Database setup

```sh
make build-db
```

Visit [localhost:80/api/v2/](localhost:80/api/v2/) to see the running API!

Each time the build script is run, it will iterate over each table in the database, wipe it, and rewrite each row using the data found in data/v2/csv.

The option to build individual portions of the database was removed in order to increase performance of the build script.

If you ever need to wipe the database use this command:

```sh
make wipe_db
```

## Docker and Compose &nbsp; [![docker hub](https://img.shields.io/docker/v/pokeapi/pokeapi?label=tag&sort=semver)](https://hub.docker.com/r/pokeapi/pokeapi)

There is also a multi-container setup, managed by [Docker Compose](https://docs.docker.com/compose/). This setup allows you to deploy a production-like environment, with separate containers for each services and is recommended if you need to simply spin up PokéAPI.

Start everything by

```sh
make docker-setup
```

If you don't have `make` on your machine you can use the following commands

```sh
docker-compose up -d
docker-compose exec -T app python manage.py migrate --settings=config.docker-compose
docker-compose exec -T app sh -c 'echo "from data.v2.build import build_all; build_all()" | python manage.py shell --settings=config.docker-compose'
```

Browse [localhost/api/v2/](http://localhost/api/v2/) or [localhost/api/v2/pokemon/bulbasaur/](http://localhost/api/v2/pokemon/bulbasaur/) on port `80`.

## GraphQL &nbsp; <a href="ttps://github.com/hasura/graphql-engine"><img height="29px" src="https://graphql-engine-cdn.hasura.io/img/powered_by_hasura_blue.svg"/></a>

When you start PokéAPI with the above docker-compose setup, an [Hasura Engine](https://github.com/hasura/graphql-engine) server is started as well. It's possible to track all the PokeAPI tables and foreign keys by simply

```sh
# hasura cli needs to be installed and available in your $PATH: https://hasura.io/docs/latest/graphql/core/hasura-cli/install-hasura-cli.html
# hasura cli's version has to be v2.0.8
make hasura-apply
```

When finished browse http://localhost:8080 and you will find the admin console. The GraphQL endpoint will be hosted at http://localhost:8080/v1/graphql.

A free public GraphiQL console is browsable at the address https://beta.pokeapi.co/graphql/console/. The relative GraphQL endpoint is accessible at https://beta.pokeapi.co/graphql/v1beta

A set of examples are provided in the directory [/graphql/examples](./graphql/examples) of this repository.

## Kubernetes &nbsp; [![k8s status](https://github.com/PokeAPI/pokeapi/actions/workflows/kustomize.yml/badge.svg?branch=master)](https://github.com/PokeAPI/pokeapi/actions/workflows/kustomize.yml)

[Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/) files are provided in the folder https://github.com/PokeAPI/pokeapi/tree/master/Resources/k8s/kustomize/base/. Create and change your secrets:

```sh
cp Resources/k8s/kustomize/base/secrets/postgres.env.sample Resources/k8s/kustomize/base/secrets/postgres.env
cp Resources/k8s/kustomize/base/secrets/graphql.env.sample Resources/k8s/kustomize/base/secrets/graphql.env
cp Resources/k8s/kustomize/base/config/pokeapi.env.sample Resources/k8s/kustomize/base/config/pokeapi.env
# Edit the newly created files
```

Configure `kubectl` to point to a cluster and then run the following commands to start a PokéAPI service.

```sh
kubectl apply -k Resources/k8s/kustomize/base/
kubectl config set-context --current --namespace pokeapi # (Optional) Set pokeapi ns as the working ns
# Wait for the cluster to spin up
kubectl exec --namespace pokeapi deployment/pokeapi -- python manage.py migrate --settings=config.docker-compose # Migrate the DB
kubectl exec --namespace pokeapi deployment/pokeapi -- sh -c 'echo "from data.v2.build import build_all; build_all()" | python manage.py shell --settings=config.docker-compose' # Build the db
kubectl wait --namespace pokeapi --timeout=120s --for=condition=complete job/load-graphql # Wait for Graphql configuration job to finish
```

This k8s setup creates all k8s resources inside the _Namespace_ `pokeapi`, run `kubectl delete namespace pokeapi` to delete them. It also creates a _Service_ of type `LoadBalancer` which is exposed on port `80` and `443`. Data is persisted on `12Gi` of `ReadWriteOnce` volumes.

## Wrappers

| Official wrapper | Repository | Features |
| --- | --- | --- |
| Node server-side | [PokeAPI/pokedex-promise-v2](https://github.com/PokeAPI/pokedex-promise-v2) | _Auto caching_ |
| Browser client-side | [PokeAPI/pokeapi-js-wrapper](https://github.com/PokeAPI/pokeapi-js-wrapper) | _Auto caching_, _Image caching_ |
| Java/Kotlin | [PokeAPI/pokekotlin](https://github.com/PokeAPI/pokekotlin) | |
| Python 2/3 | [PokeAPI/pokepy](https://github.com/PokeAPI/pokepy) | _Auto caching_ |
| Python 3 | [PokeAPI/pokebase](https://github.com/PokeAPI/pokebase) | _Auto caching_, _Image caching_ |

| Wrapper | Repository | Features |
| --- | --- | --- |
| PHP | [lmerotta/phpokeapi](https://github.com/lmerotta/phpokeapi) | _Auto caching, lazy loading_ |
| Ruby | [rdavid1099/poke-api-v2](https://github.com/rdavid1099/poke-api-v2) | |
| .Net Standard | [mtrdp642/PokeApiNet](https://github.com/mtrdp642/PokeApiNet) | _Auto caching_ |
| Go | [mtslzr/pokeapi-go](https://github.com/mtslzr/pokeapi-go) | _Auto caching_ |
| Dart | [prathanbomb/pokedart](https://github.com/prathanbomb/pokedart) | |
| Rust | [lunik1/pokerust](https://gitlab.com/lunik1/pokerust) | _Auto caching_ |
| Spring Boot | [dlfigueira/spring-pokeapi](https://github.com/dlfigueira/spring-pokeapi) | _Auto caching_ |
| Swift | [kinkofer/PokemonAPI](https://github.com/kinkofer/PokemonAPI) | |
| Typescript server-side/client-side | [Gabb-c/Pokenode-ts](https://github.com/Gabb-c/pokenode-ts) | _Auto caching_ |
| Python | [beastmatser/aiopokeapi](https://github.com/beastmatser/aiopokeapi) | _Auto caching, asynchronous_
| Scala | [juliano/pokeapi-scala](https://github.com/juliano/pokeapi-scala) | _Auto caching_ |

## Donations

Help to keep PokéAPI running! If you're using PokéAPI as a teaching resource or for a project, consider sending us a $10 donation to help keep the service up. We get 330 million requests a month!

Thank you to all our backers! [Become a backer](https://opencollective.com/pokeapi#backer)

<a href="https://opencollective.com/pokeapi#backers" target="_blank"><img src="https://opencollective.com/pokeapi/backers.svg?width=890"></a>

## Join Us On Slack!

> **Warning**
> Currently no maintainer has enough free time to support the community on Slack. Our Slack is in an unmaintained status.

Have a question or just want to discuss new ideas and improvements? Hit us up on Slack. ~~Consider talking with us here before creating a new issue.~~
This way we can keep issues here a bit more organized and helpful in the long run. Be excellent to each other :smile:

[Sign up](https://join.slack.com/t/pokeapi/shared_invite/zt-1l4vpwa8k-muQmMrFfv7TIFGrVWzjzcw) easily!

Once you've signed up visit [PokéAPI on Slack](https://pokeapi.slack.com)

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
