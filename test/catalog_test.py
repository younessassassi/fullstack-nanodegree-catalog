from flask import url_for
from flask.ext.testing import TestCase

import catalog
from catalog.models import User, Category, Item


class CatalogTestCase(TestCase):
    """Catalog test case.

    Test case to create db, then add user, category and item then assert that
    information is correct before tearing down the db

    """
    def create_app(self):
        return catalog.create_app('test')

    def setUp(self):
        self.db = catalog.db
        self.db.create_all()
        self.client = self.app.test_client()

        u = User(username='test@test.com',
                 password='test',
                 name='Testa Tester')
        c = Category(name='soccer', user=u)
        i = Item(name='ball', description='soccer ball', user=u, category=c)
        self.db.session.add(u)
        self.db.session.add(c)
        self.db.session.add(i)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
                         data=dict(username='test@test.com', password='test'))

    def tearDown(self):
        catalog.db.session.remove()
        catalog.db.drop_all()

    def test_edit_items(self):
        ctg = Category.query.first()
        assert ctg.user.name == 'Testa Tester'
        itm = Item.query.first()
        assert ctg.name == 'soccer'
        ctg_item = ctg.items[0]
        assert ctg_item == itm
        assert ctg_item.name == 'ball'
        assert itm.description == 'soccer ball'

        # response = self.client.post(
        #     url_for('items.edit', item_id=1),
        #     data=dict(
        #         name="Hat",
        #         description="cool hat"
        #     ),
        #     follow_redirects=True
        # )

        # assert response.status_code == 200

        # assert ctg.name == 'soccer'
        # assert ctg_item == itm
        # assert ctg_item.name == 'Hat'
