from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def hash_password(self):
        self.password = bcrypt.generate_password_hash(self.password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return self.admin_id

    def is_authenticated(self):
        return self.admin_id > 0

    def is_anonymous(self):
        return not self.admin_id

    def is_active(self):
        return True


class User(db.Model):
    __tablename__ = 'user'

    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_EXPIRED = 'expired'

    TYPE_ADMIN = 'admin'
    TYPE_USER = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    company = db.Column(db.String(255))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    postcode = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    locksmith_licence = db.Column(db.String(255))
    account_status = db.Column(db.String(255))
    account_type = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime)
    renewal_date = db.Column(db.DateTime)
    registration_expiry = db.Column(db.DateTime)
    registrations_max = db.Column(db.Integer, default=3)
    customer_token = db.Column(db.String(255))
    subscription_token = db.Column(db.String(255))

    def hash_password(self):
        self.password = bcrypt.generate_password_hash(self.password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.user_id > 0

    def is_anonymous(self):
        return not self.user_id

    def is_active(self):
        return True


class Device(db.Model):
    __tablename__ = 'device'
    rego_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'))
    registration_date = db.Column(db.DateTime)
    last_check_date = db.Column(db.DateTime)
    registration_key = db.Column(db.String(255))
    device_name = db.Column(db.String(255))

    user = db.relationship('User', backref='devices')


## OAuth Models ##

class Client(db.Model):
    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.user_id'))
    # required if you need to support client credential
    user = db.relationship('User')

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.user_id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
