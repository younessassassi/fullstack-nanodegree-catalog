from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user

from .import auth
from .. import db
from ..models import User
from .forms import LoginForm, SignupForm
from .oauth import OAuthSignIn

@auth.route('/login', methods=['POST', 'GET'])
def login():
	# if g.user is not None and g.user.is_authenticated():
	# 	return redirect(request.args.get('next') or url_for('items.user', username=user.username))
	form = LoginForm()
	if form.validate_on_submit():
		# login and validate the user
		user = User.get_by_username(form.username.data)
		if user is not None:
			if user.password_hash is None:
				flash('Please sign in using Google login below')
			elif user.check_password(form.password.data):
				login_user(user, form.remember_me.data)
				flash('Logged in successfully as {}.'.format(user.name))
				return redirect(request.args.get('next') or url_for('items.user', username=user.username))
			else:
				flash('incorrect username or password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
					password=form.password.data,
					name=form.name.data)
		db.session.add(user)
		db.session.commit()
		flash('Welcome, {}! Please Login'.format(user.name))
		return redirect(url_for('.login'))
	return render_template("auth/signup.html", form=form)


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
	#Flask-Login function
	if not current_user.is_anonymous():
		return redirect(url_for('main.index'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@auth.route('/callback/<provider>')
def oauth_callback(provider):
	if not  current_user.is_anonymous():
		return redirect(url_for('main.index'))
	oauth = OAuthSignIn.get_provider(provider)
	name, username = oauth.callback()
	if username is None:
		flash('Authentication failed.')
		return redirect(url_for('main.index'))

	# Look if user already exists
	user = User.get_by_username(username)
	if not user:
		# create the user.  try to use the name, but if not set, then use the portion of email
		if name is None or name == "":
			name = email.split('@')[0]

		user=User(username=username, name=name)
		db.session.add(user)
		db.session.commit()

	# Log in the user, by default remembering them for their next visit
	# unless they log out.
	login_user(user, remember=True)
	return redirect(request.args.get('next') or url_for('items.user', username=user.username))

