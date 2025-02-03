from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from ipaddress import IPv4Network, IPv4Address

from app._config import app_version

from app.extensions import *
from app.models import *
from app.forms import NewPrefixForm, NewAllocationForm

base = Blueprint('base', __name__)

@base.route('/',methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('base.dashboard'))
    else:
        return redirect(url_for('auth.login'))

@base.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    
    return render_template('panel/dashboard.html', title="Dashboard", is_dash=True, app_version=app_version)

@base.route('/network',methods=['GET','POST'])
@login_required
def networks():
    networks = Network.query.all()
    form = NewPrefixForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            network = IPv4Network(f"{str(form.subnet.data)}/{str(form.prefix.data)}")
            
            add_net = Network(network_address=str(network.network_address),prefix=network.prefixlen,hosts=network.num_addresses,description=str(form.description.data))
            db.session.add(add_net)
            db.session.commit()
            
            return redirect(url_for('base.networks'))
            
        except:
            flash("Invalid Subnet or Prefix", 'danger')
            return redirect(url_for('base.networks'))        
    elif form.errors:
        flash(form.errors, 'danger')
        
    return render_template('panel/networks.html', title="Prefixes", is_networks=True, app_version=app_version, prefixes=networks, form=form)

@base.route('/network/allocations/<int:net_id>',methods=['GET','POST'])
@login_required
def allocations(net_id):
    
    db_allocations = Allocation.query.filter_by(net_id=net_id).all()
    db_network = Network.query.filter_by(id=net_id).first()
    
    form = NewAllocationForm()
    if request.method == 'POST' and form.validate_on_submit():
        network = IPv4Network(f"{str(db_network.network_address)}/{str(db_network.prefix)}")
        if IPv4Address(form.ipv4.data) in network.hosts():
            add_alloc = Allocation(ipv4=str(form.ipv4.data),net_id=db_network.id,hostname=str(form.hostname.data),description=str(form.description.data))
            db.session.add(add_alloc)
            db.session.commit()
            return redirect(url_for('base.allocations',net_id=net_id))
        
        return 'nok'
    
    
    
    return render_template('panel/allocations.html', title="Allocations", is_networks=True, app_version=app_version, form=form, allocations=db_allocations, network=db_network)