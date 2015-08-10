from datetime import datetime

from sqlalchemy import desc, collate
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from catalog import db

''' User class representing the User table in the database '''
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), unique=True)
	name = db.Column(db.String(100) , nullable=False)
	password_hash = db.Column(db.String)
	items = db.relationship('Item', backref='user', lazy='dynamic')
	categories = db.relationship('Category', backref='user', lazy='dynamic')

	# ensure the password cannot be read
	@property 
	def password(self):
		raise AttributeError('password: write-only field')

	# generate a password hash
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	# compare the password to password hash
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	# return a user based on a username
	@staticmethod
	def get_by_username(username):
		return User.query.filter_by(username=username).first()

	# provide a clean representation of the object instance
	def __repr__(self):
		return "<User '{}' with username: '{}'>".format(self.name, self.username)


''' Category class representing the Category table in the database '''
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True , nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	items = db.relationship('Item', backref='category', lazy='dynamic')

	@staticmethod
	# retrieve the category based on its id
	def get_by_category_id(id):
		return Category.query.filter_by(id=id).first()

	@staticmethod
	# retrieve all existing categories
	def all():
		return Category.query.order_by(collate(Category.name, 'NOCASE'))

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name': self.name,
			'id': self.id,
		}

	# provide a clean representation of the object instance
	def __repr__(self):
		return "<Category '{}'>".format(self.name)


''' Item class representing the Item table in the database '''
class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True , nullable=False)
	description = db.Column(db.String(400) , nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


	@staticmethod
	# return a list of the latest added items up to a limited provided in 
	# the function argument
	def newest(num):
		return Item.query.order_by(desc(Item.date)).limit(num)

	@staticmethod
	# if item exits, return it otherwise create a new one
	def get_or_create(name):
		try:
			return Item.query.filter_by(name=name).one()
		except:
			return Item(name=name)

	@staticmethod 
	# retrieve all existing items
	def all():
		return Item.query.all()

	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'date': self.date
		}

	# provide a clean representation of the object instance
	def __repr__(self):
		return "<Item '{}'>".format(self.name)
