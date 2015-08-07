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

		u = User(username='test@test.com', password='test', name='Testa Tester')
		c = Category(name='soccer', user=u)
	 	i = Item(name='ball', description='soccer ball', user=u, category=c)
		self.db.session.add(u)
		self.db.session.add(c)
		self.db.session.add(i)
		self.db.session.commit()

		self.client.post(url_for('auth.login'),
			data = dict(username='test@test.com', password='test'))

	def tearDown(self):
		catalog.db.session.remove()
		catalog.db.drop_all()

	def test_edit_items(self):
		response = self.client.post(
			url_for('items.edit', item_id=1),
			data = dict(
				name = "Hat",
				description = "cool hat"
			),
			follow_redirects = True
		)

		assert response.status_code == 200
		ctg = Category.query.first()
		itm = Item.query.first()
		ctgItem = ctg.items[0]
		assert itm.description == 'cool hat'
		assert ctg.name == 'soccer'
		assert ctgItem == itm
		assert ctgItem.name == 'Hat'
		assert ctg.user.name == 'Testa Tester'


