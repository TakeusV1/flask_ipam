from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app._config import app_version

from app.extensions import *
from app.models import *

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