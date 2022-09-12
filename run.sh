export $(cat .venv)
cd src
../.heroku/python/bin/python manage.py migrate
../.heroku/python/bin/python manage.py collectstatic
../.heroku/python/bin/gunicorn program_automation.wsgi
