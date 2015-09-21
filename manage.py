import os

from catalog import create_app, db

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('CATALOG_ENV') or 'dev')

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("runserver", Server(port=5000, host='0.0.0.0'))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
