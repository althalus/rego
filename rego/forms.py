from flask import url_for
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from rego.models import db, User, Admin
from wtforms import fields, validators


class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise validators.ValidationError(self.message)


UserForm = model_form(User,
                      db.session,
                      Form,
                      only=[
                          'username', 'name',
                          'email', 'phone', 'company',
                          'address1', 'address2',
                          'postcode', 'city', 'country',
                          'locksmith_licence'
                      ],
                      field_args={
                          'username': {'validators': [validators.required(),
                                                      Unique(User, User.username)]},
                          'password': {'validators': [validators.required()]},
                          'name': {'validators': [validators.required()]},
                          'email': {'validators': [validators.required()]},
                          'phone': {'validators': [validators.required()]},
                          'company': {'validators': [validators.required()]},
                          'address1': {'validators': [validators.required()]},
                          'address2': {'validators': [validators.required()]},
                          'postcode': {'validators': [validators.required()]},
                          'city': {'validators': [validators.required()]},
                          'country': {'validators': [validators.required()]},
                          'locksmith_licence': {'validators': [validators.required()]},
                      })


class SignupForm(Form):
    username = fields.StringField('username', [validators.required()])
    password = fields.StringField('password', [validators.required()])
    device_id = fields.StringField('Device ID', [validators.required()])


class LoginForm(Form):
    username = fields.StringField('username', [validators.required()])
    password = fields.PasswordField('password', [validators.required()])

    def validate_username(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError("Username or password does not match")

        if not user.check_password(self.password.data):
            raise validators.ValidationError("Username or password does not match")

    def get_user(self):
        return Admin.query.filter_by(username=self.username.data).first()


class PasswordForm(Form):
    password = fields.PasswordField('Password', [validators.required(),
                                                validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = fields.PasswordField('Repeat Password')
