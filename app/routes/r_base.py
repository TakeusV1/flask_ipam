from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from ipaddress import IPv4Network

from app._config import app_version

from app.extensions import *
from app.models import *
from app.forms import NewPrefixForm

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

@base.route('/networks',methods=['GET','POST'])
@login_required
def networks():
    prefixes = Prefix.query.all()
    form = NewPrefixForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            network = IPv4Network(f"{str(form.subnet.data)}/{str(form.prefix.data)}")
            
            add_prefix = Prefix(network_address=str(network.network_address),prefix=network.prefixlen,hosts=network.num_addresses,description=str(form.description.data))
            db.session.add(add_prefix)
            db.session.commit()
            
            return f"done {network.num_addresses}"
            
        except:
            flash("Invalid Subnet or Prefix", 'danger')
            return redirect(url_for('base.networks'))        
    elif form.errors:
        flash(form.errors, 'danger')
        
    return render_template('panel/networks.html', title="Prefixes", is_networks=True, app_version=app_version, prefixes=prefixes, form=form)

@base.route('/networks/allocations/<string:network>',methods=['GET','POST'])
@login_required
def allocations(network):
    return f"Allocations for {network}"