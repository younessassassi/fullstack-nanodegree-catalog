from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

from .config import config_by_name

db = SQLAlchemy()

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

# enable debug toolbar
toolbar = DebugToolbarExtension()

# for displaying timestamps
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    # register the authorization blueprint for user login, logout and signup
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # register the categories blueprint to manage the categories
    from .categories import categories as categories_blueprint
    app.register_blueprint(categories_blueprint, url_prefix='/categories')

    # register the items blueprint for add, edit, delete and view of items
    from .items import items as items_blueprint
    app.register_blueprint(items_blueprint, url_prefix='/items')

    # register the main blueprint for index page and error handling
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app

import models
