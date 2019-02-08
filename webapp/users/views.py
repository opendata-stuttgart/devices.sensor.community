# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from urllib.parse import quote_plus
from flask import (Flask, Blueprint, render_template, current_app, request, flash, url_for, redirect, session, abort,
                   jsonify, send_from_directory)
from flask_babel import lazy_gettext as _
from flask_login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh
from ..extensions import db, mail
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer
from .forms import *
from .models import User
from . import constants
from ..external_data.models import Node

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailForm()
    if form.validate_on_submit():
        email_status = User.get_mail_status(form.email.data.lower())
        if email_status == 1:
            return redirect('/login-with-password?email=%s' % (quote_plus(form.email.data.lower())))
        elif email_status == 0:
            User.send_recover_mail(form.email.data.lower(), False)
            current_app.logger.info('%s sent an recovery request again' % (form.email.data.lower()))
            return render_template('recover-mail-sent-again.html')
        else:
            if not Node.query.filter_by(email=form.email.data.lower()).count():
                return render_template('invalid-email.html')
            else:
                return redirect('/register-minimal?email=%s' % (quote_plus(form.email.data.lower())))
    return render_template('login.html', form=form)


@users.route('/register-minimal', methods=['GET', 'POST'])
def register_minimal():
    form = MinimalRegisterForm()
    # form.email.data = request.args.get('email', '')
    form.email.data = request.form.get('email', '')
    if form.validate_on_submit():
        if User.is_email_taken(form.email.data.lower()):
            email_status = User.get_mail_status(form.email.data.lower())
            if email_status == 1:
                flash(_('Critical database error.'),
                      'success')
                return redirect('/login-with-password?email=%s' % (quote_plus(form.email.data.lower())))
            elif email_status == 0:
                User.send_recover_mail(form.email.data.lower(), False)
                current_app.logger.info('%s sent an recovery request again' % (form.email.data.lower()))
                return render_template('recover-mail-sent-again.html')
        else:
            User.send_recover_mail(form.email.data.lower(), True, True)
            current_app.logger.info('%s sent an registration request' % (form.email.data.lower()))
            return render_template('register-existing-wait-for-mail.html')
    return render_template('register-minimal.html', form=form)


@users.route('/login-with-password', methods=['GET', 'POST'])
def login_with_password():
    form = LoginForm()
    form.email.data = request.args.get('email', '')
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.email.data.lower(), form.password.data)
        if user:
            if authenticated:
                login_user(user, remember=form.remember_me.data)
                return redirect('/meine-luftdaten')
            else:
                flash(_('The password is incorrect'), 'danger')
        else:
            flash(_('This account does not exist.'), 'danger')
    return render_template('login-with-password.html', form=form)


@users.route('/recover', methods=['GET', 'POST'])
def recover():
    form = RecoverForm()
    form.email.data = request.args.get('email', '')
    if form.validate_on_submit():
        email_status = User.get_mail_status(form.email.data.lower())
        if email_status == -1:
            flash(_('This account does not exist.') , 'danger')
        elif email_status == 0:
            User.send_recover_mail(form.email.data.lower(), False)
            current_app.logger.info('%s sent an recovery request again' % (form.email.data.lower()))
            return render_template('recover-mail-sent-again.html')
        else:
            User.send_recover_mail(form.email.data.lower(), False)
            current_app.logger.info('%s sent an recovery request' % (form.email.data.lower()))
            return render_template('recover-mail-sent.html')
    return render_template('recover.html', form=form)


@users.route('/recover-check', methods=['GET', 'POST'])
def recover_check():
    serialized_data = request.args.get('id', '')
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(
            serialized_data,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=constants.RECOVER_VALID_DURATION
        )
    except:
        data = False
    if data == False:
        return render_template('recover-fail.html')
    else:
        if not len(data) == 2:
            return render_template('recover-fail.html')
        else:
            user = User.query.filter_by(id=data[0])
            if user.count() != 1:
                return render_template('recover-fail.html')
            else:
                user = user.first()
                if sha256(str.encode(user.password)).hexdigest() != data[1]:
                    return render_template('recover-fail.html')
                else:
                    form = RecoverSetForm()
                    if form.validate_on_submit():
                        user.password = form.password.data
                        user.active = True
                        db.session.add(user)
                        db.session.commit()
                        login_user(user, remember=form.remember_me.data)
                        current_app.logger.info(
                            '%s got access to his / her account after registration / recovery' % (current_user.email))
                        flash(_('Password successfully updated.') , 'success')
                        return redirect('/meine-luftdaten')
                    return render_template('recover-set-password.html', form=form, url_id=serialized_data)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('login', None)
    logout_user()
    return redirect('/')


@users.route('/my-settings', methods=['GET', 'POST'])
@users.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserDataForm(request.form, obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.add(current_user)
        db.session.commit()
        current_app.logger.info('%s updated his / her user data' % (current_user.email))
        flash(_('User data saved.'), 'success')
        return redirect('/meine-luftdaten')
    return render_template('my-settings.html', form=form)


@users.route('/my-password', methods=['GET', 'POST'])
@users.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = UserPasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            current_app.logger.info('%s updated his / her password' % (current_user.email))
            flash(_('Password saved.'), 'success')
            return redirect('/meine-luftdaten')
        else:
            flash(_('Old password not correct.'), 'danger')
    return render_template('my-password.html', form=form)
