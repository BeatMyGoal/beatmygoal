.PHONY: unit func gui test

unit:
	python manage.py test tests/testUnit*.py -v2

func:
	python manage.py test tests/testFunctional*.py -v2

gui:
	python manage.py test tests/SeleniumTests/*.py

clean:
	find . -name "*.pyc" | xargs rm

local-db:
	rm -f db.sqlite3
	python manage.py syncdb --noinput
        python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
