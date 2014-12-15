install:
	sudo pip install -r requirements.txt

setup:
	python manage.py migrate --settings=config.local
	python manage.py loaddata dev_data.json --settings=config.local

wipe_db:
	rm -rf db.sqlite3

serve:
	python manage.py runserver --settings=config.local

test:
	python manage.py test --settings=config.local

clean:
	rm -rf *.pyc
