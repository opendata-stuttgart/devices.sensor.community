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

from flask_wtf import FlaskForm
from flask_babelex import lazy_gettext as _
from wtforms import (BooleanField, TextField, HiddenField, PasswordField, DateTimeField, validators, IntegerField,
                     SubmitField)
from . import constants


class EmailForm(FlaskForm):
    email = TextField(_('E-Mail addresse'),
        [
            validators.DataRequired(
                message=_('Please enter an e-mail address.')
            ),
            validators.Email(
                message=_('Please enter a correct e-mail address.')
            )
        ]
    )
    submit = SubmitField(_('next') )


class LoginForm(FlaskForm):
    email = TextField(_('E-Mail addresse'),
        [
            validators.DataRequired(
                message=_('Please enter an e-mail address.')
            ),
            validators.Email(
                message=_('Please enter a correct e-mail address.')
            )
        ]
    )
    password = PasswordField(_('Password'),
        [
            validators.DataRequired(
                message=_('Please enter a password.')
            )
        ]
    )
    remember_me = BooleanField(_('Stay logged in.') , default=False)
    submit = SubmitField(_('login'))


class MinimalRegisterForm(FlaskForm):
    email = TextField(_('E-Mail addresse'),
        [
            validators.DataRequired(
                message=_('Please enter an e-mail address.')
            ),
            validators.Email(
                message=_('Please enter a correct e-mail address.')
            )
        ]
    )
    privacy = BooleanField(_('I agree to the <a href="/privacy-policy">Privacy policy</a>.'),
        [
            validators.DataRequired(
                message=_('Please agree to the privacy policy.')
            )
        ]
    )
    submit = SubmitField(_('register'))


class RecoverForm(FlaskForm):
    email = TextField(_('E-Mail addresse'),
        [
            validators.DataRequired(
                message=_('Please enter an e-mail address.')
            ),
            validators.Email(
                message=_('Please enter a correct e-mail address.')
            )
        ]
    )
    submit = SubmitField(_('Password request via email'))


class RecoverSetForm(FlaskForm):
    password = PasswordField(_('Password'),
        [
            validators.DataRequired(
                message=_('Please enter a password.')
            ),
            validators.Length(
                min=constants.MIN_PASSWORD_LEN,
                max=constants.MAX_PASSWORD_LEN,
                message=_('Password must consist of at least %s letters.', constants.MIN_PASSWORD_LEN)
            )
        ]
    )
    password_repeat = PasswordField(_('Password (repeat)'),
        [
            validators.DataRequired(
                message=_('Please enter a password.')
            ),
            validators.EqualTo('password', message=_('Passwords must be identical.'))
        ]
    )
    remember_me = BooleanField(_('Stay logged in.'), default=False)
    submit = SubmitField(_('Save Password'))


class UserDataForm(FlaskForm):
    first_name = TextField(_('First name'))
    last_name = TextField(_('Last name'))
    submit = SubmitField(_('Save user data'))


class UserPasswordForm(FlaskForm):
    old_password = PasswordField(_('Old Password'))
    new_password = PasswordField((_('New password')),
        [
            validators.Length(
                min=constants.MIN_PASSWORD_LEN,
                max=constants.MAX_PASSWORD_LEN,
                message=_('Password must consist of at least %s letters.', constants.MIN_PASSWORD_LEN)
            )
        ]
    )
    confirm = PasswordField(_('New password (repeat)'),
        [
            validators.DataRequired(message=_('Please enter a password.')),
            validators.EqualTo('new_password', message=_('Passwords must be identical.'))
        ]
    )
    submit = SubmitField(_('Save Password'))
