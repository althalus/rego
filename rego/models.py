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
