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
from wtforms import (BooleanField, StringField, HiddenField, PasswordField, DecimalField, DateTimeField, validators,
                     IntegerField, SubmitField, TextAreaField, SelectField)
from . import PersonalConstants
from ..common.countrycodes import country_codes


class SensorSettingsForm(FlaskForm):
    name = StringField(
        'Interner Name des Sensors (veröffentlicht wird nur die Sensor-UID)',
        [
            validators.DataRequired(
                message='Bitte geben Sie einen Sensornamen an.'
            )
        ]
    )
    street_name = StringField(
        'Straße',
        [
            validators.DataRequired(
                message='Bitte geben Sie einen Straßennamen an.'
            )
        ]
    )
    street_number = StringField('Hausnummer')
    postalcode = StringField(
        'Postleitzahl',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine Postleitzahl an.'
            )
        ]
    )
    city = StringField(
        'Ort',
        [
            validators.DataRequired(
                message='Bitte geben Sie einen Ort an.'
            )
        ]
    )
    country = SelectField(
        'Staat',
        [
            validators.DataRequired(
                message='Bitte geben Sie einen Staat an.'
            )
        ],
        choices=country_codes,
        default='DE'
    )
    lat = StringField(
        'Geographischer Längengrad',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine geographische Länge an.'
            )
        ]
    )
    lon = StringField(
        'Geographischer Breitengrad',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine geographische Breite an.'
            )
        ]
    )
    height = IntegerField(
        'Höhe des Sensors über dem Boden (in cm)',
        [
            validators.DataRequired(
                message='Bitte geben Sie die Höhe des Sensors über dem Boden an.'
            )
        ]
    )
    sensor_position = IntegerField(
        'Befestigungsort des Sensors am Haus. <p class="small">1 = auf der Gartenseite, sehr gut abgeschirmt von allen Straßen, 10 = der Sensor ist an einer Hauswand direkt an der Straße. Bei diesem Wert ist irrelevant, wie groß die Straße ist, es geht nur darum, wo der Sensor am Haus angebracht ist.</p>',
        [
            validators.DataRequired(
                message='Bitte geben Sie den Befestigungsort des Sensors an.'
            )
        ]
    )
    industry_in_area = IntegerField(
        'Wie viel verarbeitende Industrie befinden sich in 100 m Radius? <p class="small">Keine Büroflächen, sondern potentielle Feinstaubproduzenten 1 = sehr wenig, 10 = sehr viel.</p>',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine Einschätzung an.'
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message='Bitte geben Sie einen Wert von 1 bis 10 an'
            )
        ]
    )
    oven_in_area = IntegerField(
        'Wie viele private Öfen oder Kamine befinden sich in 100 m Radius? <p class="small">Riecht es in Ihrem Wohngebiet sehr nach solchem Rauch? 1 = sehr wenig, 10 = sehr viel.</p>',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine Einschätzung an.'
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message='Bitte geben Sie einen Wert von 1 bis 10 an'
            )
        ]
    )
    traffic_in_area = IntegerField(
        'Wie stark befahren sind die Straßen in 100 m Radius? <p class="small">Wie nah dran sind solche Straßen? 1 = sehr wenig weiter weg, 10 = sehr viel Verkehr direkt vor der Haustür.</p>',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine Einschätzung an.'
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message='Bitte geben Sie einen Wert von 1 bis 10 an'
            )
        ]
    )
    description = TextAreaField(
        'Kurze Beschreibung des Sensor-Standortes inkl. seiner Besonderheiten'
    )
    submit = SubmitField('Einstellungen speichern')


class SensorGiveForm(FlaskForm):
    email = StringField(
        'E-Mail Adresse des Empfängers',
        [
            validators.DataRequired(
                message='Bitte geben Sie eine E-Mail-Adresse an'
            ),
            validators.Email(
                message='Bitte geben Sie eine korrekte Mailadresse an.'
            )
        ]
    )
    submit = SubmitField('Sensor übergeben')
