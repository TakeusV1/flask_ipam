from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])