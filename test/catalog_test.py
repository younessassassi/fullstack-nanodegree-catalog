from flask import url_for
from flask.ext.testing import TestCase

import catalog
from catalog.models import User, Category, Item

class CatalogTestCase(TestCase):

	def create_app(self):
		return catalog.create_app('test')

	def setUp(self):
		self.db = catalog.db
		self.db.create_all()
		self.client = self.app.test_client()

		u = User(username='test@test.com', password='test', name='Test Tester')
		ctg = Category(name='Tennis', items='racket, tennis shoes')
		self.db.session.add(u)
		self.db.session.add(ctg)
		self.db.session.commit()

		self.client.post(url_for('auth.login'),
			data = dict(username='test@test.com', password='test'))

	def tearDown(self):
		catalog.db.session.remove()
		catalog.db.drop_all()

	def test_delete_all_items(self):
		response = self.client.post(
			url_for('items.edit', item_id=1),
			data = dict(
				category = "soccer",
				items = ""
			),
			follow_redirects = True
		)

		assert response.status_code == 200
		ctg = Category.query.first()
		assert not ctg._items

