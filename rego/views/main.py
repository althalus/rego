from flask_login import login_user, LoginManager, logout_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from rego.models import User, Admin
from rego.forms import LoginForm


main = Blueprint('main', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def user_loader(userid):
    return Admin.query.filter_by(admin_id=userid).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to do that.')
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        return redirect(request.args.get("next") or url_for('main.list_users'))
    return render_template('login.html', form=form)

@main.route('/users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@main.route('/user/<id>')
@login_required
def edit_user():
    pass

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
