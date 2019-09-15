# -*- coding: UTF-8 -*-

from flask import Flask, session, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from datetime import timedelta


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# create a LoginManager object 
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # set session life time
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=1)
    db.init_app(app)

    Bootstrap(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    login_manager.refresh_view = "auth.logout"
    login_manager.needs_refresh_message = "此次登录已超时，请重新登录。"
    login_manager.needs_refresh_message_category = "info"

    # it is good practice to time out logged-in session after specific time.
    """
    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
    """

    # create a migrate object to handle the database migarations
    migrate = Migrate(app, db)

    # register blueprints
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # configurate the maximum allowed payload of upload file
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # configure error handling
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/500')
    def error():
        abort(500)

    return app
