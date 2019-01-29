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
from flask_login import current_user
from wtforms import (BooleanField, StringField, HiddenField, PasswordField, DecimalField, DateTimeField, validators,
                     IntegerField, SubmitField, TextAreaField, SelectField, FormField)
from flask_babel import lazy_gettext as _
from . import constants
from ..common.countrycodes import country_codes


class SensorLocationForm(FlaskForm):
    street_name = StringField(
        _('Street'),
        [
            validators.DataRequired(
                message=_('Please enter the street name.'),
            )
        ]
    )
    street_number = StringField(_('Street number'))
    postalcode = StringField(
        _('Postal code'),
        [
            validators.DataRequired(
                message=_('Please enter the postal code.'),
            )
        ]
    )
    city = StringField(
        _('City'),
        [
            validators.DataRequired(
                message=_('Please enter the city name.'),
            )
        ]
    )
    country = SelectField(
        _('Country'),
        [
            validators.DataRequired(
                message=_('Please enter the country name.'),
            )
        ],
        choices=country_codes,
        default='DE'
    )
    latitude = StringField(
        _('Latitude'),
        [
            validators.DataRequired(
                message=_('Please enter the latitude.'),
            )
        ]
    )
    longitude = StringField(
        _('Longitude'),
        [
            validators.DataRequired(
                message=_('Please enter the longitude.'),
            )
        ]
    )
    industry_in_area = IntegerField(
        _('How much industrial activity is there within a 100m radius?'),
        [
            validators.DataRequired(
                message=_('Please give your estimate.'),
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description='Keine Büroflächen, sondern potentielle Feinstaubproduzenten 1 = sehr wenig, 10 = sehr viel.',
    )
    oven_in_area = IntegerField(
        _('How many private stoves or fireplaces are within a 100m radius?'),
        [
            validators.DataRequired(
                message=_('Please give your estimate.'),
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description='Riecht es in Ihrem Wohngebiet sehr nach solchem Rauch? 1 = sehr wenig, 10 = sehr viel.',
    )
    traffic_in_area = IntegerField(
        _('How much traffic is there within a 100m radius?'),
        [
            validators.DataRequired(
                message=_('Please give your estimate.'),
            ),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description='Wie nah dran sind solche Straßen? 1 = sehr wenig weiter weg, 10 = sehr viel Verkehr direkt vor der Haustür.',
    )

class SensorSettingsForm(FlaskForm):
    name = StringField(
        _('Personal sensor name'),
        [
            validators.DataRequired(
                message=_('Please enter the sensor name.'),
            )
        ],
        description=_('Only the sensor ID will be published.'),
    )
    height = IntegerField(
        _('Sensor level above ground (in cm)'),
        [
            validators.DataRequired(
                message='Bitte geben Sie die Höhe des Sensors über dem Boden an.'
            )
        ]
    )
    sensor_position = IntegerField(
        _('Sensor location relative to the traffic'),
        [
            validators.DataRequired(
                message='Bitte geben Sie den Befestigungsort des Sensors an.'
            )
        ],
        description='1 = auf der Gartenseite, sehr gut abgeschirmt von allen Straßen, 10 = der Sensor ist an einer Hauswand direkt an der Straße. Bei diesem Wert ist irrelevant, wie groß die Straße ist, es geht nur darum, wo der Sensor am Haus angebracht ist.'
    )
    location = FormField(SensorLocationForm)
    description = TextAreaField(
        _('Short description of location'),
    )
    submit = SubmitField(_('Save settings'))


class SensorGiveForm(FlaskForm):
    email = StringField(
        _("Recipient's e-mail address"),
        [
            validators.DataRequired(
                message=_("Please enter e-mail address"),
            ),
            validators.Email(
                message=_("Please enter correct e-mail address"),
            )
        ]
    )
    submit = SubmitField(_("Transfer sensor"))

    def validate_email(self, field):
        if field.data.lower().strip() == current_user.email.lower().strip():
            raise validators.ValidationError(
                _("You can't transfer the sensor to yourself"))
