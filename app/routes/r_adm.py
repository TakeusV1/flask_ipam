from datetime import datetime
from flask import Blueprint, request, render_template, flash, url_for, redirect, abort
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

from app._config import app_version

from app.extensions import *
from app.models import *
from app.forms import NewUserForm, ChangePasswordForm

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET','POST'])
@login_required
def home():
    if current_user.is_admin == False:
        return abort(403)
    
    db_users = User.query.all()    
    form = NewUserForm()
    if form.validate_on_submit() and request.method == 'POST':
        # IF user exist
        if User.query.filter_by(username=form.username.data).first() != None:
            flash("User already exist", 'warning')
            return redirect(url_for('admin.home'))
        
        is_admin = False
        is_readonly = False
        if int(form.is_admin.data) == 1:
            is_admin = True
        if int(form.is_readonly.data) == 1:
            is_readonly = True
        
        db.session.add(User(username=form.username.data, password=generate_password_hash(form.password.data), is_admin=is_admin, is_reado=is_readonly))
        db.session.commit()
        flash("User Created", 'success')
        return redirect(url_for('admin.home'))
    
    return render_template('admin/home.html', title="Admin", app_version=app_version, is_admin=True, navcolor='danger', users=db_users, form=form)
    
## MODAL ROUTES

@admin.get('/user/<int:user_id>/modal/delete')
@login_required
def user_modal_delete(user_id):
    if current_user.is_admin == False:
        return abort(403)
    
    user = User.query.get(user_id)
    modal = {
        'title': 'Delete User',
        'body': f'Are you sure you want to delete <b>{user.username}</b> user ?',
        'color': 'danger',
        'action': 'delete',
        'action_text': 'Delete',
        'action_url': url_for('admin.delete_user',user_id=user.id)
    }
    return render_template('panel/_modal.html', modal=modal)

@admin.route('/user/<int:user_id>/modal/edit', methods=['GET','POST'])
@login_required
def user_modal_edit(user_id):
    if current_user.is_admin == False:
        return abort(403)
    
    user = User.query.get(user_id)
    
    form = ChangePasswordForm()
    if form.validate_on_submit() and request.method == 'POST':
        user.password = generate_password_hash(form.password.data)
        user.is_admin = False
        user.is_reado = False
        if int(form.is_admin.data) == 1:
            user.is_admin = True
        if int(form.is_readonly.data) == 1:
            user.is_reado = True
        db.session.commit()
        flash("Informations Changed", 'success')
        return redirect(url_for('admin.home'))
    
    modal = {
        'title': 'Edit User',
        'body': f'Change Informations for <b>{user.username}</b>',
        'color': 'primary',
        'modal_type': 'form',
        'action_text': 'Save',
        'form_url': url_for('admin.user_modal_edit',user_id=user.id),
    }
    return render_template('panel/_modal.html', modal=modal, form=form)	

## MODIFICATION ROUTES

@admin.get('/user/<int:user_id>/delete')
@login_required
def delete_user(user_id):
    if current_user.is_admin == False:
        return abort(403)
    
    if User.query.filter_by(is_admin=True).count() == 1 and User.query.get(user_id).is_admin == True:
        flash("You can't delete the last admin user !", 'danger')
        return redirect(url_for('admin.home'))
    
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User Deleted", 'warning')
    return redirect(url_for('admin.home'))