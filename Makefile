.PHONY: unit func gui test

s:
	python manage.py runserver

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

coverage:
	coverage run --branch --source='core','beatmygoal' manage.py test
	coverage report -m

clean:
	find . -name "*.pyc" | xargs rm

local-db:
	rm -f db.sqlite3
	python manage.py syncdb --noinput
	python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
	python scripts/populate_db.py

demo: 
	make unit
	make func
	python manage.py test tests/SeleniumTests/{testCreateAccount.py:EditUserTest.test_create_account,testInvite.py:FavoriteTest.testEmailPreviewExists,testEditGoal.py:EditGoalTest.testEditGoal} -v2

