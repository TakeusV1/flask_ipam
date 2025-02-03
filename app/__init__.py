from flask import Flask
from flask import abort, request, jsonify, make_response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from os import environ

from app._config import *
from app.models import *

from app.extensions import *

from app.routes.r_base import base
from app.routes.r_auth import auth
from app.routes.r_adm import admin

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Configuration)
        
    login_manager.init_app(app)
    db.init_app(app)
    
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    
    with app.app_context():
        db.create_all()
    
    ## BLUEPRINTS
    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    
    ## SYSTEM ROUTES
    @app.before_request
    def before_request():
        if app_maintenance:
            return abort(503)

    @app.route('/app_info')
    def route_app_info():
        response = make_response(jsonify({'app_name': app_name, 'app_version':app_version,'release_date':app_release_date,'app_maintenance':app_maintenance,'app_debug':app_debug}), 200)
        return response

    @app.route('/app_check')
    def route_app_check():
        response = make_response(jsonify({'check': 1}), 200)
        return response

    ## ERROR ROUTES
    @app.errorhandler(401)
    def not_found(error):
        HTTP_ERROR = [
            "401",
            "Unauthorized",
            "The server could not verify that you are authorized to access the URL requested. You are not authenticated, or your browser doesn't understand how to supply the credentials required...",
            "https://takeus.ovh/static/img/login.svg"
        ]
        return render_template('srv_error.html',HTTP_ERROR=HTTP_ERROR), 401

    @app.errorhandler(403)
    def not_found(error):
        HTTP_ERROR = [
            "403",
            "Forbidden",
            "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server...",
            "https://takeus.ovh/static/img/login.svg"
        ]
        return render_template('srv_error.html',HTTP_ERROR=HTTP_ERROR), 403

    @app.errorhandler(404)
    def not_found(error):
        HTTP_ERROR = [
            "404",
            "Not Found",
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again...",
            "https://takeus.ovh/static/img/404.svg"
        ]
        return render_template('srv_error.html',HTTP_ERROR=HTTP_ERROR), 404

    @app.errorhandler(500)
    def not_found(error):
        HTTP_ERROR = [
            "500",
            "Internal Server Error",
            "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
            "https://takeus.ovh/static/img/500.svg"
        ]
        return render_template('srv_error.html',HTTP_ERROR=HTTP_ERROR), 500

    @app.errorhandler(503)
    def not_found(error):
        HTTP_ERROR = [
            "503",
            "Service Unavailable",
            "The server is temporarily unable to service your request due to maintenance downtime or capacity problems. Please try again later.",
            "https://takeus.ovh/static/img/503.svg"
        ]
        return render_template('srv_error.html',HTTP_ERROR=HTTP_ERROR), 503

    ## FLASK LOGIN
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=int(user_id)).first()
    
    return app