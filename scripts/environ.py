# Loads the environment with the Django project's settings file

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Path to the project directory
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beatmygoal.settings")
