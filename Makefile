.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


install:  # Install base requirements to run project
	pip install -r requirements.txt

dev-install:  # Install developer requirements + base requirements
	pip install -r test-requirements.txt

setup:  # Set up the project database
	python manage.py migrate --settings=config.local

wipe_db:  # Delete's the project database
	rm -rf db.sqlite3

serve:  # Run the project locally
	python manage.py runserver --settings=config.local

test:  # Run tests
	python manage.py test --settings=config.local

clean:  # Remove any pyc files
	find . -type f -name '*.pyc' -delete

migrate:  # run any outstanding migrations
	python manage.py migrate --settings=config.local

shell:  # Load a shell
	python manage.py shell --settings=config.local

format:  # Format the source code
	black .

format-check:  # Check the source code has been formatted
	black . --check
