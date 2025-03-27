# Installation GUIDE
This documentation is very good, but needs a few changes to make it work (in our case) :
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04<br>

Before starting the app ensure to intall pip packages in requirements.txt [Section](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04#step-4-configuring-gunicorn)
- `pip install Flask-Login Flask-SQLAlchemy Flask-WTF mysql-connector-python SQLAlchemy cryptography`
- You don't need to create `wsgi.py`, when asked, replace : `wsgi:app` with `'app:create_app()'` .
  - EX : For starting APP with gunicorn : `gunicorn --bind 0.0.0.0:5000 'app:create_app()'`
  - In Service File, replace "ExecStart" line with :<br>
`ExecStart=/YOUR_ENV_LOCATION/bin/gunicorn --workers 1 --bind 0.0.0.0:5000 -m 007 'app:create_app()'`<br>
_(Adjust the number of workers to your needs)_
- you must first run setup.py to create the admin user.<br>
_(it will create a second database in `./var/setup-instance`. It will have to be merged in the application database in `./var/app-instance`)_
