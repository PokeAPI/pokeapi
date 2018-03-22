install:
	pip install -r requirements.txt

dev-install:
	pip install -r test-requirements.txt

lint:
	flake8 .

setup:
	python manage.py migrate --settings=config.local
	python manage.py loaddata dev-data.json --settings=config.local

wipe_db:
	rm -rf db.sqlite3

serve:
	python manage.py runserver --settings=config.local

test:
	python manage.py test --settings=config.local

clean:
	find . -type f -name '*.pyc' -delete

migrate:
	python manage.py migrate --settings=config.local
