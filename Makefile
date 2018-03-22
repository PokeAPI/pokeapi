install:
	pip2 install -r requirements.txt

dev-install:
	pip2 install -r test-requirements.txt

lint:
	flake8 .

setup:
	python2 manage.py migrate --settings=config.local
	python2 manage.py loaddata dev-data.json --settings=config.local

wipe_db:
	rm -rf db.sqlite3

serve:
	python2 manage.py runserver --settings=config.local

test:
	python2 manage.py test --settings=config.local

clean:
	find . -type f -name '*.pyc' -delete

migrate:
	python2 manage.py migrate --settings=config.local
