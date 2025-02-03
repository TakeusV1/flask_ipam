from datetime import datetime
from flask import Blueprint, request, render_template, flash, url_for, redirect, abort
from flask_login import login_required, current_user

from app._config import app_version

from app.extensions import *
from app.models import *

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def home():
    if current_user.is_admin:
        return redirect(url_for('admin.dash'))
    else:
        return abort(403)
    
@admin.route('/dashboard')
@login_required
def dash():
    if current_user.is_admin == False:
        return abort(403)
    
    return f"Welcome {current_user.username} to the admin dashboard"