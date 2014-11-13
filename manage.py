#!/usr/bin/env python
import os

from flask.ext.script import Manager
from dash import create_app
from dash.models import db, Role, User
from flask.ext.migrate import MigrateCommand
from dash.jobs import jobs
from dash.ldap.accounts import main as run_account_sync
from dash.ldap.groups import main as run_group_sync
from flask.ext.migrate import _get_config
from alembic import command

env = os.environ.get('DASH_ENV', 'prod')
app = create_app('dash.settings.%sConfig' % env.capitalize(), env=env)


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create():
    """ Initialize the database, stamp the alembic table for future migrations,
    and make sure roles and studentnet support user exist.

    Do not run this command on an existing database unless you know what you
    are doing. """
    db.create_all()
    config = _get_config('migrations')
    command.stamp(config, 'head')
    roles = (
        ("faculty", "Teachers, and other academic staff  "),
        ("student", "Students"),
        ("alum", "Graduate students"),
        ("staff", "All staff members"),
        ("employee", "Employees who are not staff members (Contracts, for example)"),
        ("member", "Any staff, current student, or employee. Where possible, use the most accurate category instead of this one."),
        ("affiliate", "A person with a relationship to the school not otherwise described."),

    )
    current_roles = [role.name for role in Role.query.all()]
    for role, desc in roles:
        if role not in current_roles:
            role = Role(name=role, description=desc)
            db.session.add(role)
    db.session.commit()

    # Make sure studentnet admin user exists
    snsupport = User.query.filter_by(user_name='studentnetsupport').first()
    if not snsupport:
        snsupport = User(user_name='studentnetsupport',
                         email='support@studentnet.net',
                         first_name='Studentnet',
                         last_name='Support')
    snsupport.password = '5a4d12ad1f6151bc5d7a2143dafe383eae6b8629'
    snsupport.role = Role.query.filter_by(name='employee').first()
    snsupport.status = User.ADMIN
    db.session.add(snsupport)
    db.session.commit()


@manager.command
def queuerunner():
    """ Start async worker. The main async jobs are Google Apps processing. """
    jobs.work()


@manager.command
def syncaccounts():
    """ Import and synchronise Accounts information from configured sync profiles """
    run_account_sync()


@manager.command
def syncgroups():
    """ Import and synchronise Groups information from configured sync profiles """
    run_group_sync()

if __name__ == '__main__':
    manager.run()
