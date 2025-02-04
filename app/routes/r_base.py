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
    
    return render_template('panel/networks.html', title="Prefixes", is_networks=True, app_version=app_version, prefixes=networks, form=form, Allocation=Allocation)

@base.route('/network/<int:net_id>/allocations',methods=['GET','POST'])
@login_required
def allocations(net_id):
    
    active_page = request.args.get('page', type=int)
    db_network = Network.query.filter_by(id=net_id).first()
    db_allocations = db.paginate(db.select(Allocation).filter_by(net_id=net_id), per_page=15 )
        
    form = NewAllocationForm()
    if request.method == 'POST' and form.validate_on_submit():
        network = IPv4Network(f"{str(db_network.network_address)}/{str(db_network.prefix)}")
        # Check if IPv4 Address is already allocated
        if Allocation.query.filter_by(ipv4=str(form.ipv4.data)).first() != None:
            flash("IPv4 Address Already Allocated", 'danger')
            return redirect(url_for('base.allocations', net_id=net_id, page=active_page))
        # Check if IPv4 Address is in the Network
        if IPv4Address(form.ipv4.data) in network.hosts():
            add_alloc = Allocation(ipv4=str(form.ipv4.data), net_id=db_network.id, hostname=str(form.host_name.data), description=str(form.host_desc.data))
            db.session.add(add_alloc)
            db.session.commit()
            flash("Allocation Added", 'success')
            return redirect(url_for('base.allocations', net_id=net_id, page=active_page))
        # If not in Network
        flash("Invalid IPv4 Address", 'danger')
        return redirect(url_for('base.allocations', net_id=net_id, page=active_page))
    # If Form Errors
    elif form.errors:
        flash(form.errors, 'danger')
    
    return render_template('panel/allocations.html', title="Allocations", is_networks=True, app_version=app_version, form=form, allocations=db_allocations, network=db_network, Inventory=Inventory, active_page=active_page)

## MODAL ROUTES

@base.get('/network/<int:net_id>/allocations/<string:ipv4>/del_modal')
@login_required
def allocation_del_modal(net_id,ipv4):
    modal = {
        'title': 'Delete Allocation',
        'body': f'Are you sure you want to delete <b>{ipv4}</b> allocation ?',
        'color': 'warning',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('base.allocation_delete',net_id=net_id,ipv4=ipv4)
    }
    return render_template('panel/_modal.html', modal=modal, net_id=net_id, ipv4=ipv4, old_page=request.args.get('page', type=int))	

@base.get('/network/<int:net_id>/del_modal')
@login_required
def network_del_modal(net_id):
    db_network = Network.query.filter_by(id=net_id).first()
    modal = {
        'title': 'Delete Network',
        'body': f'Are you sure you want to delete <b>{db_network.network_address}/{db_network.prefix}</b> network ?',
        'color': 'danger',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('base.network_delete',net_id=net_id)
    }
    return render_template('panel/_modal.html', modal=modal, net_id=net_id)	

## DELETE ROUTES

@base.get('/network/<int:net_id>/allocations/<string:ipv4>/delete')
@login_required
def allocation_delete(net_id,ipv4):
    db_alloc = Allocation.query.filter_by(net_id=net_id,ipv4=ipv4).first()
    db.session.delete(db_alloc)
    db.session.commit()
    flash("Allocation Deleted", 'warning')
    return redirect(url_for('base.allocations',net_id=net_id,page=request.args.get('page', type=int)))

@base.get('/network/<int:net_id>/delete')
@login_required
def network_delete(net_id):
    db_network = Network.query.filter_by(id=net_id).first()
    db_alloc = Allocation.query.filter_by(net_id=db_network.id).all()
    
    if db_network != None:
        if db_alloc != None:
            for alloc in db_alloc:
                db.session.delete(alloc)
        db.session.delete(db_network)
        db.session.commit()
        flash("Network Deleted", 'warning')
        return redirect(url_for('base.networks'))            
    else:
        flash("Network Not Found", 'danger')
        return redirect(url_for('base.networks'))
