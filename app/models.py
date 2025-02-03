from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(),primary_key=True,unique=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(32),unique=True)
    is_admin = db.Column(db.Boolean(),default=False)
    dat_last = db.Column(db.DateTime())