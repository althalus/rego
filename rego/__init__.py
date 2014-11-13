import os
from flask import Flask
from models import db, migrate


def create_app(config=None, env=None):
    """
    Flask application factory. See:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        config: python path to config object
        env: Current environment. Eg prod, dev, stage
    """

    app = Flask(__name__)

    # Load config object
    if env is None:
        env = os.environ.get('DASH_ENV', 'prod')
    if config is None:
        config = 'dash.settings.%sConfig' % env.capitalize()

    app.config.from_object(config)

    # Optionally, load extra config from file
    if os.environ.get('DASH_SETTINGS', None):
        app.config.from_envvar('DASH_SETTINGS')

    # Set up plugins
    db.init_app(app)
    migrate.init_app(app, db)

    if app.debug:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    # register blueprints
    from views.main import main
    app.register_blueprint(main)

    from main.api import api
    api.init_app(app)

    from main.saml import saml
    app.register_blueprint(saml, url_prefix='/saml')

    # Load extra jinja stuff
    app.jinja_env.add_extension('jinja2.ext.do')

    return app

if __name__ == '__main__':
    env = os.environ.get('DASH_ENV', 'prod')
    app = create_app('dash.settings.%sConfig' % env.capitalize(), env=env)
