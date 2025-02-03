from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_turnstile import Turnstile

login_manager = LoginManager()

db = SQLAlchemy()
turnstile = Turnstile()