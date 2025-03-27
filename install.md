# Installation GUIDE
This documentation is very good, but needs a few changes to make it work (in our case) :
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04<br>

Before starting the app ensure to install pip packages in requirements.txt Referrenced [Section](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04#step-4-configuring-gunicorn)
- `pip install Flask-Login Flask-SQLAlchemy Flask-WTF mysql-connector-python SQLAlchemy cryptography`
- Update the configuration file under _app/\_config.py_.
  - `app_ip = '127.0.0.1'` to `app_ip = '0.0.0.0'` for easy web access.
  - Update **SECRET_KEY='CHANGE_ME'** variable, `openssl rand -hex 32` can be used to create a random key.
- You don't need to create or continue with the `wsgi.py` section. When asked, replace: `wsgi:app` with `'app:create_app()'` .
  - EX : For starting APP with gunicorn : `gunicorn --bind 0.0.0.0:5000 'app:create_app()'`
    - For any troubleshooting, you can add `--preload` at the end of the command for verbose logging.
  - In Service File, replace "ExecStart" line with :<br>
`ExecStart=/YOUR_ENV_LOCATION/bin/gunicorn --workers 1 --bind 0.0.0.0:5000 -m 007 'app:create_app()'`<br>
_(Adjust the number of workers to your needs)_
- you must first run setup.py to create the admin user.<br>
_(it will create a second database in `./var/setup-instance`. It will have to be merged in the application database in `./var/app-instance`)_
