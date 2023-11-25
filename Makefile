veekun_pokedex_repository = ../pokedex
local_config = --settings=config.local
docker_config = --settings=config.docker-compose
HASURA_GRAPHQL_ADMIN_SECRET=pokemon

.PHONY: help
.SILENT:

help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  # Install base requirements to run project
	pip install -r requirements.txt

dev-install:  # Install developer requirements + base requirements
	pip install -r test-requirements.txt

setup:  # Set up the project database
	python manage.py migrate ${local_config}

build-db:  # Build database
	echo "from data.v2.build import build_all; build_all()" | python manage.py shell ${local_config}

wipe-sqlite-db:  # Delete's the project database
	rm -rf db.sqlite3

serve:  # Run the project locally
	python manage.py runserver ${local_config}

test:  # Run tests
	python manage.py test ${local_config}

clean:  # Remove any pyc files
	find . -type f -name '*.pyc' -delete

migrate:  # Run any outstanding migrations
	python manage.py migrate ${local_config}

make-migrations:  # Create migrations files if schema has changed
	python manage.py makemigrations ${local_config}

shell:  # Load a shell
	python manage.py shell ${local_config}

docker-up:  # (Docker) Create services/volumes/networks
	docker-compose up -d

docker-migrate:  # (Docker) Run any pending migrations
	docker-compose exec -T app python manage.py migrate ${docker_config}

docker-build-db:  # (Docker) Build the database
	docker-compose exec -T app sh -c 'echo "from data.v2.build import build_all; build_all()" | python manage.py shell ${docker_config}'

docker-make-migrations:  # (Docker) Create migrations files if schema has changed
	docker-compose exec -T app sh -c 'python manage.py makemigrations ${docker_config}'

docker-flush-db:  # (Docker) Removes all the data present in the database but preserves tables and migrations
	docker-compose exec -T app sh -c 'python manage.py flush --no-input ${docker_config}'

docker-destroy-db:  # (Docker) Removes the volume where the database is installed on, alongside to the container itself
	docker rm -f pokeapi_db_1
	docker volume rm pokeapi_pg_data

docker-shell:  # (Docker) Launch an interative shell for the pokeapi container
	docker-compose exec app sh -l

docker-stop:  # (Docker) Stop containers
	docker-compose stop

docker-down:  # (Docker) Stop and removes containers and networks
	docker-compose down

docker-test:  # (Docker) Run tests
	docker-compose exec -T app python manage.py test ${local_config}

docker-prod:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f Resources/compose/docker-compose-prod-graphql.yml up -d

docker-setup: docker-up docker-migrate docker-build-db  # (Docker) Start services, prepare the latest DB schema, populate the DB

format:  # Format the source code
	black .

format-check:  # Check the source code has been formatted
	black . --check

pull:
	git checkout master
	git pull

pull-veekun:
	git -C ${veekun_pokedex_repository} checkout master-pokeapi
	git -C ${veekun_pokedex_repository} pull

sync-from-veekun: pull pull-veekun  # Copy data from ../pokedex to this repository
	cp -a ${veekun_pokedex_repository}/pokedex/data/csv/. ./data/v2/csv

sync-to-veekun: pull pull-veekun  # Copy data from this repository to ../pokedex
	cp -a ./data/v2/csv/. ${veekun_pokedex_repository}/pokedex/data/csv

# read-env-file:  # Exports ./.env into shell environment variables
# 	export `egrep -v '^#' .env | xargs`

hasura-export:  # Export Hasura configuration
	hasura md export --project graphql --admin-secret ${HASURA_GRAPHQL_ADMIN_SECRET}

hasura-apply:  # Apply local Hasura configuration
	hasura md apply --project graphql --admin-secret ${HASURA_GRAPHQL_ADMIN_SECRET}

hasura-get-anon-schema:  # Dumps GraphQL schema
	gq http://localhost:8080/v1/graphql --introspect > graphql/schema.graphql

kustomize-apply:  # (Kustomize) Run kubectl apply -k on the connected k8s cluster
	kubectl apply -k Resources/k8s/kustomize/base/

kustomize-staging-apply:  # (Kustomize) Run kubectl apply -k on the connected k8s cluster
	kubectl apply -k Resources/k8s/kustomize/staging/

k8s-migrate:  # (k8s) Run any pending migrations
	kubectl exec --namespace pokeapi deployment/pokeapi -- python manage.py migrate --settings=config.docker-compose

k8s-build-db:  # (k8s) Build the database
	kubectl exec --namespace pokeapi deployment/pokeapi -- sh -c 'echo "from data.v2.build import build_all; build_all()" | python manage.py shell --settings=config.docker-compose'

k8s-delete:  # (k8s) Delete pokeapi namespace
	kubectl delete namespace pokeapi

start-graphql-prod:
	git pull origin master
	git submodule update --init
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f Resources/compose/docker-compose-prod-graphql.yml up -d

update-graphql-data-prod:
	git pull origin master
	git submodule update --init
	docker stop pokeapi_graphql-engine_1
	sync; echo 3 > /proc/sys/vm/drop_caches
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f Resources/compose/docker-compose-prod-graphql.yml up -d app
	make docker-migrate
	make docker-build-db
	docker stop pokeapi_app_1
	sync; echo 3 > /proc/sys/vm/drop_caches
	docker exec pokeapi_web_1 sh -c 'rm -rf /tmp/cache/*'
	docker start pokeapi_graphql-engine_1
