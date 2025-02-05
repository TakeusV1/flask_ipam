from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, IPAddress, NumberRange

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    
class NewPrefixForm(FlaskForm):
    subnet = StringField(validators=[DataRequired(),IPAddress(ipv4=True),Length(max=128)])
    prefix = IntegerField(validators=[DataRequired(),NumberRange(min=20,max=32)])
    description = StringField(validators=[Length(max=128)])
    
class NewAllocationForm(FlaskForm):
    ipv4 = StringField(validators=[DataRequired(),IPAddress(ipv4=True),Length(max=128)])
    host_name = StringField(validators=[Length(max=128)])
    host_desc = StringField(validators=[Length(max=128)])
    #host_type = SelectField(choices=[(0,'None'),(1,'Computer'),(2,'Server'),(3,'Virtual Machine'),(4,'Network Device'),(5,'Other')],validators=[DataRequired()])
    
class NewUserForm (FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    is_admin = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    is_admin = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    
class ChangeAllocationForm(FlaskForm):
    hostname = StringField(validators=[Length(max=128)])
    description = StringField(validators=[Length(max=128)])