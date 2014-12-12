from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, LoginManager, logout_user, login_required
from rego.models import User
from rego.forms import LoginForm

login = Blueprint('login', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def user_loader(userid):
    return User.query.filter_by(user_id=userid).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to do that.')
    return redirect(url_for('login.signin'))


@login.route('/login', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        return redirect(request.args.get("next") or url_for('admin.list_users'))
    return render_template('login.html', form=form)


@login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
