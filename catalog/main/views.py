from flask import render_template

from . import main
from .. import login_manager

from ..models import User, Category, Item

@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@main.route('/')
def index():
	return render_template('index.html', new_items=Item.newest(10))


@main.app_errorhandler(403)
def page_not_found(e):
	return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@main.app_errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

@main.app_context_processor
def inject_items():
	return dict(all_items=Item.all)