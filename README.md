beatmygoal
==========

Local Installation Instructions
-------------------------------
- set up the virtualenv and install packages (see below)
- To run the app: `python manage.py syncdb`, followed by `python manage.py runserver`
- To run tests: `python manage.py test -v2`
- To populate the DB with some test data: `python manage.py shell < scripts/populate_db.py`

To set up and update venv:
- Create your own venv using `virtualenv venv` (venv/* is ignored in the .gitignore file)
- `source venv/bin/activate`
- Use `pip install --allow-all-external -r requirements.txt` to download site packages
  - JP: I had to add ARCHFLAGS based on this post [http://stackoverflow.com/questions/22312583/cant-install-mysql-gem-on-os-x]

Heroku instructions
-------------------------------
To update to heroku:
- make sure you have Heroku Toolbelt
- `heroku login`
- `heroku git:remote --app beatmygoal`
- `git push heroku master`

Heroku and database:
- The environment variable "ON_HEROKU" is used to determine whether to use PostGres or SQLite 
  (`settings.py`)
  - If for some reason this stops working, reset it with `heroku config:set ON_HEROKU=1`
- To delete the heroku database: `heroku pg:reset DATABASE_URL`
- Then, to create a new one: `heroku run python manage.py syncdb`
- Then, populate with data in any way. For example:
  `heroku run python manage.py shell < scripts/populate_db.py`
- Alternatively, for "automatic changes" you can migrate using South
  -  http://south.readthedocs.org/en/latest/tutorial/part1.html


Instruction to Use Coverage.py 
-------------------------------

- Install coverage.py by typing “pip install coverage”
- To confirm that the coverage is installed correctly, command “coverage-version”
- Run the test with the coverage command, “coverage run --source='core','beatmygoal' manage.py test” 
	- (Since we are using unit-test and functional-test, we only need to check the files in ‘core’ and ‘beatmygoal’, which contain url, models, and views.)
- Then, call the report, “coverage report -m” 
	- (‘-m flag’ shows the line numbers of missing statements)
- The missing columns tell us which lines are not covered by our unit-test and functional-test
- To delete the previous report, type “coverage erase”