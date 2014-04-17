.PHONY: unit func gui test

hook:
	cp scripts/pre-commit .git/hooks/
	cp scripts/post-merge .git/hooks/
	chmod +x .git/hooks/pre-commit
	chmod +x .git/hooks/post-merge

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
	python manage.py shell < scripts/populate_db.py
	@echo -e "\n"

