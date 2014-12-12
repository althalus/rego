from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from rego.models import db, User, Device
from rego.forms import UserForm, PasswordForm
from functools import wraps
from flask_login import current_user

admin = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.account_type != User.TYPE_ADMIN:
            return "Unauthorized", 403
        else:
            return f(*args, **kwargs)

    return decorator


@admin.route('/users')
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)


@admin.route('/user/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.filter_by(user_id=id).first()
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.edit_user", id=id))
    return render_template('users/edit.html', user=user, form=form)


@admin.route('/user/<id>/change_password', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password(id):
    user = User.query.filter_by(user_id=id).first()
    form = PasswordForm(obj=user)
    if form.validate_on_submit():
        user.password = form.password.data
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.edit_user', id=id))
    return render_template('users/change_password.html', user=user, form=form)


@admin.route('/user/<id>/registrations')
@login_required
@admin_required
def list_registrations(id):
    user = User.query.filter_by(user_id=id).first()
    return render_template('registrations/list.html', user=user)


@admin.route('/registration/<id>/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_registration(id):
    rego = Device.query.filter_by(rego_id=id).first()
    user = rego.user
    if request.method == 'POST':
        db.session.delete(rego)
        db.session.commit()
        return redirect(url_for('admin.list_registrations', id=user.user_id))
    return render_template('registrations/delete.html')
