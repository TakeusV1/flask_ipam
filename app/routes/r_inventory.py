from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from app.extensions import *
from app.models import *
from app.forms import NewInventoryItem, ChangeInventoryItem

inventory = Blueprint('inventory', __name__)

@inventory.route('/add', methods=['GET','POST'])
@login_required
def add_item():
    if current_user.is_reado:
        return abort(403)
    
    form = NewInventoryItem()
    if form.validate_on_submit() and request.method == 'POST':
            add_net = Inventory(host_type=int(form.item_type.data),host_name=str(form.item_name.data),host_desc=str(form.item_desc.data))
            db.session.add(add_net)
            db.session.commit()
            flash("Item ADDED", 'success')
    
    return render_template('panel/inventory_add.html', title='ADD ITEM', form=form, navcolor='success')
    
@inventory.route('/list/<int:item_type>', methods=['GET','POST'])
@login_required
def list_items(item_type):
    if item_type == 5:
        db_items = Inventory.query.all()
    else:
        db_items = Inventory.query.filter_by(host_type=item_type).all()
    
    if item_type == 0:
        title = 'Others'
    elif item_type == 1:
        title = 'Computers'
    elif item_type == 2:
        title = 'Servers'
    elif item_type == 3:
        title = 'VM\'s'
    elif item_type == 4:
        title = 'Network'
    else:
        title = 'All'
    
    return render_template('panel/inventory_view.html', title=title, item_list=db_items, current_page=item_type, navcolor='success')

@inventory.route('/action/<int:item_id>/<int:action>', methods=['GET','POST'])
@login_required
def action_item(item_id,action):
    if current_user.is_reado:
        return abort(403)
    
    if action == 1:
        db_item = Inventory.query.filter_by(id=item_id).first()
        db_allocs = Allocation.query.filter_by(device_id=db_item.id).all()
        # Delete Link Allocation(s)
        if db_allocs != []:
            for alloc in db_allocs:
                alloc.device_id = None
                
        db.session.delete(db_item)
        db.session.commit()
    
        return redirect(url_for('inventory.list_items',item_type=request.args.get('page', type=int)))

## MODAL ROUTES

@inventory.get('/<int:item_id>/view_modal')
@login_required
def item_view_modal(item_id):
    db_item = Inventory.query.filter_by(id=item_id).first()
    modal = {
        'title': f'Informations of <b>{db_item.host_name}</b> ({db_item.id})',
        'modal_type': 'infos',
        'color': 'info',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('inventory.action_item',item_id=item_id,action=1)
    }
    
    if db_item.host_type == 0:
        host_type = 'Others'
    elif db_item.host_type == 1:
        host_type = 'Computers'
    elif db_item.host_type == 2:
        host_type = 'Servers'
    elif db_item.host_type == 3:
        host_type = 'VM\'s'
    elif db_item.host_type == 4:
        host_type = 'Network'
    else:
        host_type = 'Error'
    
    informations = [
        ('Type',host_type,'col-6'),
        ('Name',db_item.host_name,'col-6'),
        ('Description',db_item.host_desc,'col-6'),
        ('Model',db_item.host_model,'col-6'),
        ('Manufacturer',db_item.host_manufacturer,'col-6'),
        ('SerialNumber',db_item.host_serialnumber,'col-6'),
        ('OS',db_item.host_os,'col-6'),
        ('Location',db_item.host_location,'col-6'),
        ('Owner',db_item.host_owner,'col-6'),
        ('Contact',db_item.host_contact,'col-6'),
        ('Allocations',db_item.host_allocations,'col-12'),
    ]
    
    return render_template('panel/_modal.html', modal=modal, item_id=item_id, informations=informations, old_page=request.args.get('page', type=int), pagination_active=True)

@inventory.get('/<int:item_id>/del_modal')
@login_required
def item_del_modal(item_id):
    db_item = Inventory.query.filter_by(id=item_id).first()
    modal = {
        'title': 'Delete Item',
        'body': f'Are you sure you want to delete <b>{db_item.host_name}</b> ?',
        'color': 'danger',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('inventory.action_item',item_id=item_id,action=1)
    }
    return render_template('panel/_modal.html', modal=modal, item_id=item_id, old_page=request.args.get('page', type=int), pagination_active=True)

@inventory.route('/<int:item_id>/edit_modal', methods=['GET','POST'])
@login_required
def item_edit_modal(item_id):
    if current_user.is_reado:
        return abort(403)
    
    db_item = Inventory.query.filter_by(id=item_id).first()
        
    form = ChangeInventoryItem()
    if form.validate_on_submit() and request.method == 'POST':
        
        db_item.host_type = form.item_type.data
        db_item.host_name = form.item_name.data
        # Description
        if form.item_desc.data != '' and form.item_desc.data != 'None':
            db_item.host_desc = form.item_desc.data
        else:
            db_item.host_desc = None
        # Model
        if form.item_model.data != '' and form.item_model.data != 'None':
            db_item.host_model = form.item_model.data
        else:
            db_item.host_model = None
        # Manufacturer
        if form.item_manufacturer.data != '' and form.item_manufacturer.data != 'None':
            db_item.host_manufacturer = form.item_manufacturer.data
        else:
            db_item.host_serialnumber = None
        # Serial Number
        if form.item_serial_number.data != '' and form.item_serial_number.data != 'None':
            db_item.host_serialnumber = form.item_serial_number.data
        else:
            db_item.host_serialnumber = None
        # OS
        if form.item_os.data != '' and form.item_os.data != 'None':
            db_item.host_os = form.item_os.data
        else:
            db_item.host_os = None
        # Location
        if form.item_location.data != '' and form.item_location.data != 'None':
            db_item.host_location = form.item_location.data
        else:
            db_item.host_location = None
        # Owner
        if form.item_owner.data != '' and form.item_owner.data != 'None':
            db_item.host_owner = form.item_owner.data
        else:
            db_item.host_owner = None
        # Contact
        if form.item_contact.data != '' and form.item_contact.data != 'None':
            db_item.host_contact = form.item_contact.data
        else:
            db_item.host_contact = None
        
        # Allocations
        db_existing_allocs = Allocation.query.filter_by(device_id=db_item.id).all()
        # Unlink old Allocation(s)
        if db_existing_allocs != []:
            for alloc in db_existing_allocs:
                    alloc.device_id = None
                    
        if form.item_ip_allocations.data != '' and form.item_ip_allocations.data != 'None':

            allocs = form.item_ip_allocations.data.split(',')
            put_allocs_db = ""
            for alloc in allocs:
                db_alloc = Allocation.query.filter_by(ipv4=alloc).first()
                if db_alloc != None:
                    put_allocs_db += db_alloc.ipv4+','
                    db_alloc.device_id = db_item.id
                elif allocs[-1] == '':
                    pass
                else:
                    flash('Unknown IPv4', 'warning')
                    return redirect(url_for('inventory.list_items',item_type=request.args.get('page', type=int)))
                    
            db_item.host_allocations = put_allocs_db
                
        else:       
            db_item.host_allocations = None
        
        db.session.commit()
        flash("Item Updated", 'success')
        return redirect(url_for('inventory.list_items',item_type=request.args.get('page', type=int)))

    # Setting default values
    form.item_name.default = db_item.host_name
    form.item_desc.default = db_item.host_desc
    form.item_type.default = db_item.host_type
    form.item_model.default =db_item.host_model
    form.item_manufacturer.default = db_item.host_manufacturer
    form.item_serial_number.default = db_item.host_serialnumber
    form.item_os.default = db_item.host_os
    form.item_location.default = db_item.host_location
    form.item_owner.default = db_item.host_owner
    form.item_contact.default = db_item.host_contact
    form.item_ip_allocations.default = db_item.host_allocations
    form.process()
    
    modal = {
        'title': 'Update Item',
        'body': f'Change informations for <b>{db_item.host_name}</b>.',
        'color': 'primary',
        'modal_type': 'form',
        'action_text': 'Save',
        'form_url': url_for('inventory.item_edit_modal',item_id=item_id),
        'inventory':True,
    }
    
    return render_template('panel/_modal.html', modal=modal, form=form, old_page=request.args.get('page', type=int), pagination_active=True)	