from flask import render_template

from . import main
from .. import login_manager

from ..models import User, Category, Item


@login_manager.user_loader
def load_user(userid):
    """get user based on userId """
    return User.query.get(int(userid))


@main.route('/')
def index():
    """return template with all categories and the latest items"""
    return render_template('main/index.html',
                           new_items=Item.newest(10),
                           new_categories=Category.all())


@main.app_errorhandler(403)
def insufficient_permissions(e):
    """return custom 403 error template """
    return render_template('main/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """return custom 404 error template """
    return render_template('main/404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    """return custom 403 error template """
    return render_template('main/500.html'), 500


@main.app_context_processor
def inject_categories():
    """inject all categories for templates use """
    return dict(all_categories=Category.all)
