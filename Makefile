install:
	pip install -r requirements.txt --upgrade

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
	rm -rf *.pyc
