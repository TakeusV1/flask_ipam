from datetime import datetime
from flask import Blueprint, request, render_template, flash, abort, redirect, url_for, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app._config import *

from app.extensions import *
from app.models import *
from app.forms import LoginForm

auth = Blueprint('auth', __name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user != None:
            if user.password != None:
                if check_password_hash(user.password,form.password.data):
                    login_user(user)
                    
                    user.dat_last = datetime.now()
                    db.session.commit()
                    
                    return redirect(url_for("base.dashboard"))

        flash("Bad username or password !", 'danger')
        return render_template("auth/login.html", title="Login", form=form, bad_password=True)
    return render_template('auth/login.html', title="Login", form=form)

@auth.route("/change",methods=['GET','POST'])
@login_required
def change():
    pass

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))