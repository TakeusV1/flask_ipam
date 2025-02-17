from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from flask_login import login_required, current_user
from ipaddress import IPv4Network, IPv4Address

from app._config import app_version

from app.extensions import *
from app.models import *
from app.forms import NewInventoryItem

inventory = Blueprint('inventory', __name__)

@inventory.route('/add', methods=['GET','POST'])
@login_required
def add_item():
    form = NewInventoryItem()
    if form.validate_on_submit() and request.method == 'POST':
            add_net = Inventory(host_type=int(form.item_type.data),host_name=str(form.item_name.data),host_desc=str(form.item_desc.data))
            db.session.add(add_net)
            db.session.commit()
            flash("Item ADDED", 'success')
    
    return render_template('panel/inventory_add.html', title='ADD ITEM', form=form)
    
@inventory.route('/list/<int:item_type>', methods=['GET','POST'])
@login_required
def list_items(item_type):
    db_items = Inventory.query.filter_by(host_type=item_type).all()
    return render_template('panel/inventory_view.html', Title='View Items', item_list=db_items)

@inventory.route('/action/<int:item_id>/<int:action>', methods=['GET','POST'])
@login_required
def action_item(item_id,action):
    
    if action == 1:
        db_item = Inventory.query.filter_by(id=item_id).first()
        
        db.session.delete(db_item)
        db.session.commit()
    
    return redirect(url_for('base.dashboard'))