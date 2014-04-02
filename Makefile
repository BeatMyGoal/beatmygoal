.PHONY: unit func gui test

unit:
	python manage.py test -p "testUnit*" -v2

func:
	python manage.py test -p "testFunc*" -v2

gui:
	python manage.py test -p "gui*" -v2

clean:
	find . -name "*.pyc" | xargs rm

