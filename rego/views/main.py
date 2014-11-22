from flask_login import login_user, LoginManager, logout_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from rego.models import db, User, Admin
from rego.forms import LoginForm, UserForm, PasswordForm


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
def edit_user(id):
    user = User.query.filter_by(user_id=id).first()
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.edit_user", id=id))
    return render_template('users/edit.html', user=user, form=form)


@main.route('/user/<id>/change_password', methods=['GET', 'POST'])
@login_required
def change_password(id):
    user = User.query.filter_by(user_id=id).first()
    form = PasswordForm(obj=user)
    if form.validate_on_submit():
        user.password = form.password.data
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.edit_user', id=id))
    return render_template('users/change_password.html', user=user, form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
