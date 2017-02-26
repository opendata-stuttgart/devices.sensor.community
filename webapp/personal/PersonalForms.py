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
from wtforms import (BooleanField, TextField, HiddenField, PasswordField, DecimalField, DateTimeField, validators, IntegerField, SubmitField, TextAreaField)
from . import PersonalConstants

class SensorSettingsForm(FlaskForm):
  name = TextField(
    'Name des Sensors',
    [
      validators.Required(
        message='Bitte geben Sie einen Sensornamen an.'
      )
    ]
  )
  street_name = TextField(
    'Straße',
    [
      validators.Required(
        message='Bitte geben Sie einen Straßennamen an.'
      )
    ]
  )
  street_number = TextField('Hausnummer')
  postalcode = TextField(
    'Postleitzahl',
    [
      validators.Required(
        message='Bitte geben Sie eine Postleitzahl an.'
      )
    ]
  )
  city = TextField(
    'Ort',
    [
      validators.Required(
        message='Bitte geben Sie einen Ort an.'
      )
    ]
  )
  lat = TextField(
    'Geographischer Längengrad',
    [
      validators.Required(
        message='Bitte geben Sie eine geographische Länge an.'
      )
    ]
  )
  lon = TextField(
    'Geographischer Breitengrad',
    [
      validators.Required(
        message='Bitte geben Sie eine geographische Breite an.'
      )
    ]
  )
  node_height = IntegerField(
    'Höhe des Sensors über dem Boden (in cm)',
    [
      validators.Required(
        message='Bitte geben Sie die Höhe des Sensors über dem Boden an.'
      )
    ]
  )
  description = TextAreaField(
    'Kurze Beschreibung des Sensor-Standortes inkl. seiner Besonderheiten'
  )
  submit = SubmitField('Einstellungen speichern')

class SensorGiveForm(FlaskForm):
  email = TextField(
    'E-Mail Adresse des Empfängers',
    [
      validators.Required(
        message='Bitte geben Sie eine E-Mail-Adresse an'
      ),
      validators.Email(
        message='Bitte geben Sie eine korrekte Mailadresse an.'
      )
    ]
  )
  submit = SubmitField('Sensor übergeben')