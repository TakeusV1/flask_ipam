from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, IPAddress

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    
class NewPrefixForm(FlaskForm):
    subnet = StringField(validators=[DataRequired(),IPAddress(ipv4=True),Length(max=128)])
    prefix = SelectField(choices=[(30,'/30'),(29,'/29'),(28,'/28'),(27,'/27'),(26,'/26'),(25,'/25'),(24,'/24'),(23,'/23'),(22,'/22')],validators=[DataRequired()])
    vlan_id = IntegerField()
    description = StringField(validators=[Length(max=128)])
    
class NewUserForm(FlaskForm):
    username = StringField(validators=[DataRequired(),Length(max=128)])
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    is_admin = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    is_readonly = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired(),Length(max=128)])
    is_admin = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    is_readonly = SelectField(choices=[(0,'No'),(1,'Yes')],validators=[DataRequired()])
    
class ChangeAllocationForm(FlaskForm):
    hostname = StringField(validators=[Length(max=128)])
    description = StringField(validators=[Length(max=128)])
    is_special = SelectField(choices=[(0,'None'),(1,'DHCP'),(2,'Gateway')],validators=[DataRequired()],label='Special USE ?')

class NewInventoryItem(FlaskForm):
    item_name = StringField(validators=[DataRequired(),Length(max=64)])
    item_desc = StringField(validators=[Length(max=64)])
    item_type = SelectField(choices=[(1,'Computer'),(2,'Server'),(3,'Virtual Machine'), (4,'Network Device'), (0,'Other')],validators=[DataRequired()])
    
class ChangeInventoryItem(FlaskForm):
    item_name = StringField(validators=[DataRequired(),Length(max=64)])
    item_desc = StringField(validators=[Length(max=64)])
    item_type = SelectField(choices=[(1,'Computer'),(2,'Server'),(3,'Virtual Machine'), (4,'Network Device'), (0,'Other')],validators=[DataRequired()])
    # Hardware Information
    item_model = StringField(validators=[Length(max=64)])
    item_manufacturer = StringField(validators=[Length(max=64)])
    item_serial_number = StringField(validators=[Length(max=64)])
    # Network Information
    item_os = StringField(validators=[Length(max=64)])
    item_location = StringField(validators=[Length(max=64)])
    item_owner = StringField(validators=[Length(max=64)])
    item_contact = StringField(validators=[Length(max=64)])
    # Allocation(s)
    item_ip_allocations = StringField()