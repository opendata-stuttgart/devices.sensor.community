# encoding: utf-8

"""
Copyright (c) 2012 - 2016, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask_wtf import FlaskForm
from wtforms import (BooleanField, TextField, HiddenField, PasswordField, DateTimeField, validators, IntegerField, SubmitField)
from . import UserConstants

class EmailForm(FlaskForm):
  email = TextField(
    'E-Mail Adresse',
    [
      validators.Required(
        message='Bitte geben Sie eine E-Mail-Adresse an'
      ),
      validators.Email(
        message='Bitte geben Sie eine korrekte Mailadresse an.'
      )
    ]
  )
  submit = SubmitField('weiter')

class LoginForm(FlaskForm):
  email = TextField(
    'E-Mail Adresse',
    [
      validators.Required(
        message='Bitte geben Sie eine E-Mail-Adresse an'
      ),
      validators.Email(
        message='Bitte geben Sie eine korrekte Mailadresse an.'
      )
    ]
  )
  password  = PasswordField(
    'Passwort',
    [
      validators.Required(
        message='Bitte geben Sie ein Passwort ein.'
      )
    ]
  )
  remember_me = BooleanField( 'Eingeloggt bleiben', default = False)
  submit = SubmitField('login')

class MinimalRegisterForm(FlaskForm):
  email = TextField(
    'E-Mail Adresse',
    [
      validators.Required(
        message='Bitte geben Sie eine E-Mail-Adresse an'
      ),
      validators.Email(
        message='Bitte geben Sie eine korrekte Mailadresse an.'
      )
    ]
  )
  privacy = BooleanField(
    'Ich stimme den <a href="/datenschutz">Datenschutzbestimmungen</a> zu',
    [
      validators.Required(
        message='Bitte stimmen Sie den Datenschutzbestimmungen zu.'
      )
    ]
  )
  submit = SubmitField('registrieren')

class RecoverForm(FlaskForm):
  email = TextField(
    'E-Mail Adresse',
    [
      validators.Required(
        message='Bitte geben Sie eine E-Mail-Adresse an'
      ),
      validators.Email(
        message='Bitte geben Sie eine korrekte Mailadresse an.'
      )
    ]
  )
  submit = SubmitField('Password via E-Mail anfordern')

class RecoverSetForm(FlaskForm):
  password = PasswordField(
    'Passwort', 
    [
      validators.Required(
        message='Bitte geben Sie ein Passwort ein.'
      ),
      validators.Length(
        min=UserConstants.MIN_PASSWORD_LEN,
        max=UserConstants.MAX_PASSWORD_LEN,
        message='Passwort muss aus mindestens %s Buchstaben bestehen.' % (UserConstants.MIN_PASSWORD_LEN)
      )
    ]
  )
  password_repeat = PasswordField(
    'Passwort (Wiederholung)',
    [
      validators.Required(
        message='Bitte geben Sie ein Passwort ein.'
      ),
      validators.EqualTo('password', message='Passwörter müssen identisch sein.')
    ]
  )
  remember_me = BooleanField( 'Anschließend eingeloggt bleiben', default = False)
  submit = SubmitField('Passwort speichern')
  
class UserDataForm(FlaskForm):
  first_name = TextField( 'Vorname' )
  last_name = TextField( 'Nachname' )
  submit = SubmitField('Nutzerdaten speichern')

class UserPasswordForm(FlaskForm):
  old_password = PasswordField(
    'Altes Passwort'
  )
  new_password = PasswordField(
    'Neues Passwort', 
    [
      validators.Length(
        min=UserConstants.MIN_PASSWORD_LEN,
        max=UserConstants.MAX_PASSWORD_LEN,
        message='Passwort muss aus mindestens %s Buchstaben bestehen.' % (UserConstants.MIN_PASSWORD_LEN)
      )
    ]
  )
  confirm = PasswordField(
    'Neues Passwort (Wiederholung)',
    [
      validators.Required(message='Bitte geben Sie ein Passwort ein.'),
      validators.EqualTo('new_password', message='Passwörter müssen identisch sein.')
    ]
  )
  submit = SubmitField('Passwort speichern')
