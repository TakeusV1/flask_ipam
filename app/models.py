from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(),primary_key=True,unique=True)
    username = db.Column(db.String(16),unique=True)
    password = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean(),default=False)
    is_reado = db.Column(db.Boolean(),default=False)
    ui_theme = db.Column(db.String(16))
    dat_last = db.Column(db.DateTime())
    
class Network(db.Model):
    id = db.Column(db.Integer(),primary_key=True,unique=True)
    vlan_id = db.Column(db.Integer())
    prefix = db.Column(db.Integer())
    network_address = db.Column(db.String(16),unique=True)
    hosts = db.Column(db.Integer())
    description = db.Column(db.String(32))
    is_blacklisted = db.Column(db.Boolean(),default=False)
    
class Allocation(db.Model):
    ipv4 = db.Column(db.String(16),primary_key=True,unique=True)
    net_id = db.Column(db.Integer(),db.ForeignKey('network.id'))
    hostname = db.Column(db.String(32))
    description = db.Column(db.String(64))
    is_used = db.Column(db.Boolean(),default=False)
    is_dhcp = db.Column(db.Boolean(),default=False)
    is_gateway = db.Column(db.Boolean(),default=False)
    is_decom = db.Column(db.Boolean(),default=False)
    device_id = db.Column(db.Integer(),db.ForeignKey('inventory.id'))
    
class Inventory(db.Model):
    id = db.Column(db.Integer(),primary_key=True,unique=True)
    # Host Information
    host_type = db.Column(db.Integer())
    host_name = db.Column(db.String(64))
    host_desc = db.Column(db.String(64))
    # Hardware Information
    host_model = db.Column(db.String(64))
    host_manufacturer = db.Column(db.String(64))
    host_serialnumber = db.Column(db.String(64))
    # Network Information
    host_os = db.Column(db.String(64))
    host_location = db.Column(db.String(64))
    host_owner = db.Column(db.String(64))
    host_contact = db.Column(db.String(64))
    ## Allocation(s)
    host_allocations = db.Column(db.Text())
    ### Others
    host_notes = db.Column(db.Text())