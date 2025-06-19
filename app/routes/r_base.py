from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app._config import app_version, app_theme

from app.extensions import *
from app.models import *

base = Blueprint('base', __name__)

@base.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('base.dashboard'))
    else:
        return redirect(url_for('auth.login'))

@base.route('/dashboard')
@login_required
def dashboard():
    
    db_networks = Network.query.count()
    db_inventory = Inventory.query.count()
    db_users = User.query.count()
    available_alloc = 0
    db_allocations = 0
    
    for network in Network.query.all():
        if network.is_blacklisted == False:
            available_alloc += int(network.hosts)
            db_allocations += Allocation.query.filter_by(net_id=network.id, is_used=True).count()
    
    return render_template(
        'panel/dashboard.html',
        title="Dashboard", 
        is_dash=True, 
        app_version=app_version,
        ## Variables
        db_networks=db_networks,
        db_allocations=db_allocations,
        db_inventory=db_inventory,
        available_alloc=available_alloc,
        db_users=db_users,
        Inventory=Inventory,
        navcolor='dark'
    )
    
@base.route("/theme/<string:name>",methods=['GET','POST'])
@login_required
def change_theme(name):
    if name in app_theme:
        current_user.ui_theme = name
        db.session.commit()
        return redirect(url_for('base.dashboard'))
    return 'Invalid theme name', 400