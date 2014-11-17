#!/usr/bin/env python
import os

from flask.ext.script import Manager
from rego import create_app
from flask.ext.migrate import MigrateCommand

env = os.environ.get('REGO_ENV', 'prod')
app = create_app('rego.settings.%sConfig' % env.capitalize(), env=env)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
