# encoding: utf-8

"""
Copyright (c) 2018, Maintainer: David Lackovic
based on Ernesto Ruge https://github.com/ruhrmobil-E/meine-luftdaten/
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask import (current_app, render_template)
from werkzeug import generate_password_hash, check_password_hash
from flask_babel import lazy_gettext as _

from passlib.hash import bcrypt
from passlib import pwd
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask_login import UserMixin
from ..common.helpers import JsonSerializer, get_current_time
from ..extensions import db, mail
from . import constants

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# class UserRoles(db.Model):
#   __tablename__ = 'roles_users'
#   id = db.Column(db.Integer(), primary_key=True)
#   user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#   role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    _password = db.Column('password', db.String(constants.PW_STRING_LEN), nullable=False)
    active = db.Column(db.Boolean, default=False)
    privacy = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    updated = db.Column(db.DateTime, nullable=False, default=get_current_time)

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.email

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        print(password)
        self._password = bcrypt.hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return bcrypt.verify(password, self.password)

    def has_role(self, role_to_check):
        for role in self.roles:
            if role.name == role_to_check:
                return True
        return False

    @classmethod
    def authenticate(cls, email, password):
        user = User.query.filter(db.or_(User.email == email)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def is_email_taken(cls, email):
        return bool(User.query.filter_by(email=email).count())

    @classmethod
    def get_mail_status(cls, email):
        user = User.query.filter_by(email=email)
        if not user.count():
            return -1
        else:
            user = user.first()
            if user.active:
                return 1
            else:
                return 0

    @classmethod
    def send_recover_mail(cls, email, create_user, privacy=False):
        if create_user:
            user = User()
            user.email = email
            user.password = pwd.genword(length=16)
            user.active = False
        else:
            user = User.query.filter_by(email=email)
            if user.count() != 1:
                return False
            user = user.first()
        if privacy:
            user.privacy = True
        db.session.add(user)
        db.session.commit()
        recover_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        recover_url = "%s/recover-check?id=%s" % (
            current_app.config['PROJECT_URL'],
            recover_serializer.dumps([user.id, sha256(str.encode(user.password)).hexdigest()],
                                     salt=current_app.config['SECURITY_PASSWORD_SALT'])
        )
        msg = Message(
            _('Create account to configure the fine dust sensor.'),
            sender=current_app.config['MAILS_FROM'],
            recipients=[email],
            html=render_template('emails/register-existing.html' if create_user else 'emails/recover.html',
                                 recover_url=recover_url)
            )
        mail.send(msg)
        return True


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), unique=True)
    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    updated = db.Column(db.DateTime, nullable=False, default=get_current_time)

    def __repr__(self):
        return '<Role %r>' % self.name
