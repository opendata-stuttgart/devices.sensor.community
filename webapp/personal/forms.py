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
from wtforms.fields import FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_babel import lazy_gettext as _
from . import constants
from ..common.countrycodes import country_codes

from webapp.external_data.models import SensorType, db


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
        description='No office space, but potential fine dust producers 1 = very little, 10 = very much.',
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
        description='Does it smell very much like such smoke in your area? 1 = very little, 10 = very much.',
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
        description='How close are those roads? 1 = very little further away, 10 = a lot of traffic right on your doorstep.',
    )

def fetch_sensor_types():
    # Custom order just to pronounce default types
    return SensorType.query.order_by(db.case([
            (SensorType.uid.in_(['SDS011', 'DHT22']), 1),
        ], else_=0).desc()).all()

class SensorForm(FlaskForm):
    pin = StringField(_('PIN'))
    sensor_type = QuerySelectField(_('Sensor Type'),
                                   query_factory=fetch_sensor_types)

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
                message='Please indicate the height of the sensor above the ground.'
            )
        ]
    )
    sensor_position = IntegerField(
        _('Sensor location relative to the traffic'),
        [
            validators.DataRequired(
                message='Please indicate the mounting location of the sensor.'
            )
        ],
        description='1 = on the garden side, very well shielded from all streets, 10 = the sensor is on a house wall directly on the street. With this value it is irrelevant how big the street is, it is only about where the sensor is attached to the house.'
    )
    location = FormField(SensorLocationForm)
    sensors = FieldList(FormField(SensorForm), min_entries=1)
    description = TextAreaField(
        _('Short description of location'),
    )
    submit = SubmitField(_('Save settings'))


class SensorRegisterForm(SensorSettingsForm):
    sensor_id = StringField(_('Sensor ID'))


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
