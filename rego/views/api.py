from flask.ext.restful import Api, Resource
from rego.models import db, User, Device
from rego.forms import UserForm, SignupForm
from flask import request
import datetime


class SignupAPI(Resource):
    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            user.hash_password()
            user.registration_date = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
        else:
            return {'errors': form.errors}, 406


class LoginAPI(Resource):
    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.value).first()
            if user.check_password(form.password):
                if len(user.devices) > user.registrations_max:
                    return {'errors': 'Maximum registrations reached'}, 401
                device = Device()
                device.user = user
                device.registration_id = form.device_id
                device.registration_date = datetime.datetime.now()
                db.session.add(device)
                db.session.commit()

            return {'errors': 'Bad username or password'}, 401
        return {'errors': form.errors}, 406


class CheckAPI(Resource):
    def get(self):
        device = Device.query.filter_by(registration_id=request.params.get('device')).first()
        if not device:
            return {'errors': 'Device not registered'}, 401
        user = device.user
        if user.account_status != User.STATUS_ACTIVE:
            return {'errors': 'Account not active'}, 401


api = Api(prefix='/api')
api.add_resource(SignupAPI, '/signup', endpoint='signup')
api.add_resource(LoginAPI, '/login', endpoint='login')
api.add_resource(CheckAPI, '/check', endpoint='check')
