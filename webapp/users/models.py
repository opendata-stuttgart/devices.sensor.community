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
from flask_babelex import lazy_gettext as _

from flask_security import UserMixin, RoleMixin
from ..common.helpers import get_current_time
from ..extensions import db, mail
from . import constants

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    active = db.Column(db.Boolean, default=False)
    privacy = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    updated = db.Column(db.DateTime, nullable=False, default=get_current_time)
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def has_role(self, role_to_check):
        for role in self.roles:
            if role.name == role_to_check:
                return True
        return False

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


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(255))

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    updated = db.Column(db.DateTime, nullable=False, default=get_current_time)
