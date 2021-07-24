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

from flask import request, current_app as app
from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, validators,
                     IntegerField, SubmitField, TextAreaField, SelectField, FormField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import FieldList

from webapp.common.helpers import RequiredIf
from webapp.external_data.models import SensorType, db
from ..common.countrycodes import country_codes


def default_country():
    """Try returning sensible default country value based on user browser
    accepted languages"""

    try:
        return request.accept_languages.best_match(dict(country_codes).keys())
    except Exception:
        return 'DE'


class SensorLocationForm(FlaskForm):
    indoor = BooleanField(_("Indoor Sensor"), )

    street_name = StringField(_('Street *'), [RequiredIf(indoor=False, message=_('Please enter the street name.'))])
    street_number = StringField(_('Street number'))

    postalcode = StringField(_('Postal code *'), [RequiredIf(indoor=False, message=_('Please enter the postal code.'))])

    city = StringField(_('City *'), [RequiredIf(indoor=False, message=_('Please enter the city name.'))])

    country = SelectField(
        _('Country *'),
        [
            validators.InputRequired(
                message=_('Please enter the country name.'),
            ),
            validators.NoneOf(['--'], message=_('Please enter the country name.'), )
        ],
        choices=country_codes,
    )

    latitude = StringField(_('Latitude'), default="0.0",
                           validators=[RequiredIf(indoor=False, message=_('Please enter the latitude.'))])
    longitude = StringField(_('Longitude'), default="0.0",
                            validators=[RequiredIf(indoor=False, message=_('Please enter the longitude.'))])

    industry_in_area = IntegerField(
        _('How much industrial activity is there within a 100m radius?'),
        [
            # validators.InputRequired(
            #     message=_('Please give your estimate.'),
            # ),
            validators.Optional(),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description=_('No office space, but potential fine dust producers 1 = very little, 10 = very much.'),
    )
    oven_in_area = IntegerField(
        _('How many private stoves or fireplaces are within a 100m radius?'),
        [
            # validators.InputRequired(
            #     message=_('Please give your estimate.'),
            # ),
            validators.Optional(),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description=_('Does it smell very much like such smoke in your area? 1 = very little, 10 = very much.'),
    )
    traffic_in_area = IntegerField(
        _('How much traffic is there within a 100m radius?'),
        [
            # validators.InputRequired(
            #     message=_('Please give your estimate.'),
            # ),
            validators.Optional(),
            validators.NumberRange(
                min=1,
                max=10,
                message=_('Please enter the number between 1 and 10'),
            )
        ],
        description=_(
            'How close are those roads? 1 = very little further away, 10 = a lot of traffic right on your doorstep.'),
    )


def fetch_sensor_types():
    # Custom order just to pronounce default types
    return SensorType.query.order_by(SensorType.uid.asc()).filter(
        SensorType.id.in_(app.config["SENSOR_TYPES"].keys())).all()


class SensorForm(FlaskForm):
    pin = StringField(
        _('PIN'), [validators.Optional()],
        description=_('For special use only'))

    sensor_type = QuerySelectField(
        _('Sensor Type'), [validators.Optional()],
        query_factory=fetch_sensor_types)

    def validate(self, *args, **kwargs):
        if not self.pin.data and self.sensor_type.data \
                and self.sensor_type.data.id in app.config['SENSOR_TYPES']:
            self.pin.data = app.config['SENSOR_TYPES'].get(
                self.sensor_type.data.id)
        return super().validate(*args, **kwargs)


class SensorSettingsForm(FlaskForm):
    name = StringField(
        _('Personal sensor name'),
        [
            validators.InputRequired(
                message=_('Please enter the sensor name.'),
            )
        ],
        description=_('Only the sensor ID will be published.'),
    )
    height = IntegerField(
        _('Sensor level above ground (in cm)'),
        [
            # validators.InputRequired(
            #     message='Please indicate the height of the sensor above the ground.'
            # )
            validators.Optional()
        ],
        description=_('NOT height above sea level!')
    )
    sensor_position = IntegerField(
        _('Sensor location relative to the traffic'),
        [
            # validators.InputRequired(
            #     message='Please indicate the mounting location of the sensor.'
            # )
            validators.Optional()
        ],
        description=_(
            '1 = on the garden side, very well shielded from all streets, 10 = the sensor is on a house wall directly on the street. With this value it is irrelevant how big the street is, it is only about where the sensor is attached to the house.')
    )
    exact_location = BooleanField(
        _('Publish exact location'),
        description=_('Reveal exact sensor location in public data and archives.'),
    )
    inactive = BooleanField(
        _('Inactive'),
        description=_('Mark sensor as inactive. No notifications will be sent when sensor goes offline.')
    )
    location = FormField(SensorLocationForm)
    sensors = FieldList(FormField(SensorForm), min_entries=1)

    description = TextAreaField(
        _('Short description of location'),
    )
    submit = SubmitField(_('Save settings'))


class SensorRegisterForm(SensorSettingsForm):
    sensor_id = StringField(
        _('Sensor ID'), [
            validators.InputRequired(),
            validators.Regexp('^[0-9a-fA-F]+$', message=_('Sensor ID may only contain digits and letters A to F')),
        ],
        description=_('The numeric part of the sensorname only')
    )
    sensor_board = SelectField(
        _('Sensor Board'), [validators.InputRequired()],
        choices=[('esp8266-', 'esp8266'), ('esp32-', 'esp32'), ('raspi-', 'raspi'), ('respire-', 'respire'),
                 ('smogomierz-', 'smogomierz'), ('TTN-', 'TTN')],
        default='esp8266-',
        description=_(
            'Normally this should be esp8266. Users of ESP32 boards, Raspberry PI or the Smogomierz sensor version need to change this accordingly. Also in these cases the Sensor ID is the numeric part of the name only.')
    )


class SensorGiveForm(FlaskForm):
    email = StringField(
        _("Recipient's e-mail address"),
        [
            validators.InputRequired(
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


class SensorDeleteForm(FlaskForm):
    submit = SubmitField(_("Delete sensor"))


class SensorAddForm(SensorForm):
    sensors = FieldList(FormField(SensorForm), min_entries=1)
    submit = SubmitField(_("Add sensor"))

