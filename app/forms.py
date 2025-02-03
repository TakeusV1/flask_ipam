from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, IPAddress, NumberRange

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    
class NewPrefixForm(FlaskForm):
    subnet = StringField(validators=[DataRequired(),IPAddress(ipv4=True),Length(max=128)])
    prefix = IntegerField(validators=[DataRequired(),NumberRange(min=0,max=32)])
    description = StringField(validators=[DataRequired(),Length(max=128)])