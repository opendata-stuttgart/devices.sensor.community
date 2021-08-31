# encoding: utf-8

from flask import (Blueprint, render_template, current_app, request, flash, redirect)
from flask_babelex import lazy_gettext as _
from flask_login import login_required, current_user
from flask_security.forms import ChangePasswordForm

from .forms import *
from ..extensions import db

users = Blueprint('users', __name__)


@users.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserDataForm(request.form, obj=current_user)
    change_password_form = ChangePasswordForm()

    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()
        current_app.logger.info('%s updated his / her user data' % current_user.email)
        flash(_('User data saved'), 'success')
    elif change_password_form.validate_on_submit():
        flash(_('Password changed'), 'success')
        return render_template('/settings.html')
    return render_template('my-settings.html', form=form, change_password_form=change_password_form)
