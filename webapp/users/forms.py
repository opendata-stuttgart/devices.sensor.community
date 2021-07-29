# encoding: utf-8

from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (BooleanField, TextField, PasswordField, validators, SubmitField)

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


class RecoverForm(FlaskForm):
    email = TextField(_('E-Mail address'),
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

