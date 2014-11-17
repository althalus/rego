from flask.ext.restful import Api, Resource
from rego.models import db, User, Device
from rego.forms import UserForm
from flask import request


class SignupAPI(Resource):
    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()


class LoginAPI(Resource):
    pass


class CheckAPI(Resource):
    pass


api = Api(prefix='/api')
api.add_resource(SignupAPI, '/signup', endpoint='signup')
api.add_resource(LoginAPI, '/login', endpoint='login')
api.add_resource(CheckAPI, '/check', endpoint='check')
