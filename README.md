beatmygoal
==========

To set up and update venv:
- Create your own venv using `virtualenv venv` (venv/* is ignored in the .gitignore file)
- `source venv/bin/active`
- Use `pip install --allow-all-external -r requirements.txt` to download site packages

To update to heroku:
- make sure you have Heroku Toolbelt
- `heroku login`
- `heroku git:remote --app beatmygoal`
- `git push heroku master`



