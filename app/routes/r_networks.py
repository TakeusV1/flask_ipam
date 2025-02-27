from flask import Blueprint, request, render_template, flash, redirect, url_for, session, abort
from flask_login import login_required, current_user
from ipaddress import IPv4Network, IPv4Address

from app._config import app_version

from app.extensions import *
from app.models import *
from app.forms import NewPrefixForm, ChangeAllocationForm

network = Blueprint('network', __name__)

@network.route('/',methods=['GET','POST'])
@login_required
def networks():
    networks = Network.query.all()
    form = NewPrefixForm()
    if current_user.is_reado == False:
        if request.method == 'POST' and form.validate_on_submit():
            try:
                network = IPv4Network(f"{str(form.subnet.data)}/{str(form.prefix.data)}", False)
                
                add_net = Network(network_address=str(network.network_address),prefix=network.prefixlen,hosts=network.num_addresses-2,description=str(form.description.data))
                db.session.add(add_net)
                db.session.commit()
                
                for ip in network.hosts():
                    db.session.add(Allocation(ipv4=str(ip), net_id=add_net.id))
                
                db.session.commit()
                return redirect(url_for('network.networks'))
                
            except:
                flash("Invalid Subnet or Prefix", 'danger')
                return redirect(url_for('network.networks'))        
        elif form.errors:
            flash(form.errors, 'danger')
    
    return render_template('panel/networks.html', title="Prefixes", is_networks=True, app_version=app_version, prefixes=networks, form=form, Allocation=Allocation, navcolor='dark')

@network.route('/<int:net_id>/allocations',methods=['GET','POST'])
@login_required
def allocations(net_id):
    
    active_page = request.args.get('page', type=int)
    if active_page == None:
        active_page = 1
    
    next_page = active_page+1
    prev_page = active_page-1
    
    if request.args.get('items', type=int) != None:
        session['items'] = request.args.get('items', type=int)
    try:
        if session['items'] == None:
            session['items'] = 15
    except:
        session['items'] = 15
    
    db_network = Network.query.filter_by(id=net_id).first()
    db_allocations = db.paginate(db.select(Allocation).filter_by(net_id=net_id), per_page=session['items'] )
    
    return render_template('panel/allocations.html', title="Allocations", is_networks=True, app_version=app_version, allocations=db_allocations, network=db_network, Inventory=Inventory, active_page=active_page, next_page=next_page, prev_page=prev_page, navcolor='dark')

## MODAL ROUTES

@network.get('/<int:net_id>/del_modal')
@login_required
def network_del_modal(net_id):
    db_network = Network.query.filter_by(id=net_id).first()
    modal = {
        'title': 'Delete Network',
        'body': f'Are you sure you want to delete <b>{db_network.network_address}/{db_network.prefix}</b> network ?',
        'color': 'danger',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('network.network_delete',net_id=net_id)
    }
    return render_template('panel/_modal.html', modal=modal, net_id=net_id)	

@network.get('/<int:net_id>/allocations/<string:ipv4>/del_modal')
@login_required
def allocation_del_modal(net_id,ipv4):
    modal = {
        'title': 'Remove Allocation',
        'body': f'Are you sure you want to remove <b>{ipv4}</b> allocation ?',
        'color': 'warning',
        'action': 'delete',
        'action_text': 'Remove',
        'action_url': url_for('network.allocation_delete',net_id=net_id,ipv4=ipv4)
    }
    return render_template('panel/_modal.html', modal=modal, net_id=net_id, ipv4=ipv4, old_page=request.args.get('page', type=int), pagination_active=True)	


@network.route('/<int:net_id>/allocations/<string:ipv4>/edit_modal', methods=['GET','POST'])
@login_required
def allocation_edit_modal(net_id, ipv4):
    if current_user.is_reado:
        return abort(403)
    
    db_alloc = Allocation.query.filter_by(ipv4=ipv4).first()
        
    form = ChangeAllocationForm()
    if form.validate_on_submit() and request.method == 'POST':
        db_alloc.hostname = str(form.hostname.data)
        db_alloc.description = str(form.description.data)
        db_alloc.is_used = True
        # Special Allocation
        if int(form.is_special.data) == 1:
            # DHCP
            db_alloc.is_dhcp = True
            db_alloc.is_gateway = False
            db_alloc.hostname = None
            db_alloc.description = "DHCP Allocation"
        elif int(form.is_special.data) == 2:
            # Gateway
            db_alloc.is_dhcp = False
            db_alloc.is_gateway = True
        else:
            # None
            db_alloc.is_dhcp = False
            db_alloc.is_gateway = False

        db.session.commit()
        flash("Allocation Updated", 'success')
        return redirect(url_for('network.allocations',net_id=net_id,page=request.args.get('page', type=int)))
    
    modal = {
        'title': 'Update Allocation',
        'body': f'Change informations for <b>{db_alloc.ipv4}</b> allocation.',
        'color': 'primary',
        'modal_type': 'form',
        'action_text': 'Save',
        'form_url': url_for('network.allocation_edit_modal',net_id=db_alloc.net_id,ipv4=db_alloc.ipv4),
    }
    
    old_page = request.args.get('page', type=int)
    if old_page == 0:
        old_page = 1
    
    form.hostname.default = db_alloc.hostname
    form.description.default = db_alloc.description
    if db_alloc.is_dhcp:
        form.is_special.default = 1
    elif db_alloc.is_gateway:
        form.is_special.default = 2
    form.process()
    
    return render_template('panel/_modal.html', modal=modal, form=form, old_page=old_page, pagination_active=True)	

## MODIFICATION ROUTES
@network.get('/<int:net_id>/allocations/<string:ipv4>/unallocate')
@login_required
def allocation_delete(net_id,ipv4):
    if current_user.is_reado:
        return abort(403)
    
    db_alloc = Allocation.query.filter_by(net_id=net_id,ipv4=ipv4).first()
    db_alloc.is_used = False
    db_alloc.hostname = None
    db_alloc.description = None
    db_alloc.is_dhcp = False
    db_alloc.is_gateway = False
    db.session.commit()
    flash("Allocation Removed", 'warning')
    return redirect(url_for('network.allocations',net_id=net_id,page=request.args.get('page', type=int)))

@network.get('/<int:net_id>/allocations/<string:ipv4>/decom/<int:action>')
@login_required
def allocation_decom(net_id,ipv4,action):
    if current_user.is_reado:
        return abort(403)
    
    db_alloc = Allocation.query.filter_by(net_id=net_id,ipv4=ipv4).first()
    if action == 1:
        db_alloc.is_decom = True
    else:
        db_alloc.is_decom = False
    db.session.commit()
    return redirect(url_for('network.allocations',net_id=net_id,page=request.args.get('page', type=int)))

@network.get('/<int:net_id>/delete')
@login_required
def network_delete(net_id):
    if current_user.is_reado:
        return abort(403)
    
    db_network = Network.query.filter_by(id=net_id).first()
    db_alloc = Allocation.query.filter_by(net_id=db_network.id).all()
    
    if db_network != None:
        if db_alloc != None:
            for alloc in db_alloc:
                db.session.delete(alloc)

        db.session.delete(db_network)
        db.session.commit()
        flash("Network Deleted", 'warning')
        return redirect(url_for('network.networks'))            
    else:
        flash("Network Not Found", 'danger')
        return redirect(url_for('network.networks'))

## HTMX SEARCH
@network.post('/<int:net_id>/allocations/search')
@login_required
def allocation_search(net_id):
    search = str(request.form['search']).lower() 
      
    db_network = Network.query.filter_by(id=net_id).first()
    db_alloc = Allocation.query.filter_by(net_id=net_id).all()
    obj_list = []
    
    # Advance Search
    if '*' in search:
        search = search.split("*")[1]
        # AND
        if ',' in search:            
            for alloc in db_alloc:
                if alloc.ipv4.lower() in search.split(','):
                    obj_list.append(alloc)
        # BETWEEN
        if '-' in search:
            search = search.split('-')
            if search[0].split('.')[-1] == '' or search[1].split('.')[-1] == '':
                return "Invalid(s) Number(s)"
            temp_1 = int(search[0].split('.')[-1])
            temp_2 = int(search[1].split('.')[-1])
            
            for alloc in db_alloc:
                if int(alloc.ipv4.split('.')[-1]) <= temp_2 and int(alloc.ipv4.split('.')[-1]) >= temp_1:
                    obj_list.append(alloc)
        # DHCP
        if 'dhcp' in search:
            for alloc in db_alloc:
                if alloc.is_dhcp:
                    obj_list.append(alloc)
    
        ## GATEWAY
        if 'gateway' in search:
            for alloc in db_alloc:
                if alloc.is_gateway:
                    obj_list.append(alloc)
        
        ## DECOM
        if 'decom' in search:
            for alloc in db_alloc:
                if alloc.is_decom:
                    obj_list.append(alloc)
        
        ## Used
        if 'used' in search:
            for alloc in db_alloc:
                if alloc.is_used and alloc.is_dhcp == False:
                    obj_list.append(alloc)
        
    else:
        # BASIC SEARCH
        for alloc in db_alloc:
            if alloc.ipv4.lower().startswith(search):
                obj_list.append(alloc)
            elif alloc.hostname != None:
                if alloc.hostname.lower().startswith(search):
                    obj_list.append(alloc)
            elif alloc.description != None:
                if alloc.description.lower().startswith(search):
                    obj_list.append(alloc)
    
    return render_template('panel/_table-alloc.html',allocations=obj_list,Inventory=Inventory,network=db_network)