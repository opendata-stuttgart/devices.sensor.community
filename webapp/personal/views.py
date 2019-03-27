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

from flask import (Flask, Blueprint, render_template, current_app, flash, url_for, redirect, session)
from flask_login import current_user, login_required
from flask_mail import Message
from flask_babel import lazy_gettext as _
import requests
import dateutil.parser
from datetime import datetime, timedelta
import pytz

from .forms import SensorGiveForm, SensorSettingsForm, SensorRegisterForm
from ..external_data.models import Node, SensorLocation, Sensor, SensorType
from ..common.helpers import get_object_or_404, model_to_dict
from ..extensions import mail, db


personal = Blueprint('personal', __name__)

VALUE_TYPES = {
    'P1': ('µg/m³', _('Fine dust 10 µm')),
    'P2': ('µg/m³', _('Fine dust 2.5 µm')),
    'humidity': ('% RH', _('Humidity')),
    'temperature': ('°C', _('Temperature')),
}


@personal.route('/meine-luftdaten')
@personal.route('/dashboard')
@login_required
def dashboard():
    return render_template('meine-luftdaten.html')


@personal.route('/my-sensors')
@personal.route('/sensors')
@login_required
def sensor_list():
    return render_template('my-sensors.html', nodes=current_user.nodes)


@personal.route('/my-sensor/<id>/data')
@personal.route('/sensors/<id>/data')
@login_required
def sensor_data(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    sensors = node.sensors
    for sensor in sensors:
        if sensor.sensor_type_id == 14:
            sensor.sensor_type_name = 'Feinstaub-Sensor SDS011'
        elif sensor.sensor_type_id == 9:
            sensor.sensor_type_name = 'Feuchtigkeits- und Temperatur-Sensor DHT22'

        try:
            sensor_request = requests.get('http://api.luftdaten.info/static/v1/sensor/%s/' % (sensor.id))
            sensor_request.raise_for_status()
            sensor_request = sensor_request.json()
            if not sensor_request:
                continue
        except:
            continue

        sensor.data = sensor_request[0]
        if sensor.data['timestamp']:
            sensor.data['timestamp'] = dateutil.parser.parse(sensor.data['timestamp']).replace(
                tzinfo=pytz.UTC)
        if sensor.data['sensordatavalues']:
            for sensor_value in sensor.data['sensordatavalues']:
                if sensor_value['value_type'] in VALUE_TYPES:
                    unit, name = VALUE_TYPES[sensor_value['value_type']]
                    sensor_value['value_type_unit'] = unit
                    sensor_value['value_type_name'] = name
                else:
                    sensor_value['value_type_unit'] = ''
                    sensor_value['value_type_name'] = sensor_value['value_type']

    return render_template('my-sensor-data.html', node=node, sensors=sensors)


@personal.route('/my-sensor/<id>/settings', methods=['GET', 'POST'])
@personal.route('/sensors/<id>/settings', methods=['GET', 'POST'])
@login_required
def sensor_settings(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    form = SensorSettingsForm(obj=node)

    if form.validate_on_submit():
        update_delta = timedelta(
            seconds=current_app.config['SENSOR_LOCATION_UPDATE_INTERVAL'])

        if node.location.modified > datetime.utcnow() - update_delta:
            # This node's location has been modified recently, update it in
            # place
            form.populate_obj(node)
        else:
            old_location = node.location
            node.location = SensorLocation()
            form.populate_obj(node)

            location_fields = [f.short_name for f in form.location.form]
            new_d = model_to_dict(node.location, only_fields=location_fields)
            old_d = model_to_dict(old_location, only_fields=location_fields)
            if old_d == new_d:
                # No location field has been changed, revert back to original
                node.location = old_location

        db.session.commit()
        current_app.logger.info('%s updated node %s' % (current_user.email, id))
        flash(_('Settings saved successfully.'), 'success')
        return redirect(url_for('.sensor_list'))

    return render_template('my-sensor-settings.html', node=node, form=form)


@personal.route('/sensors/register', methods=['GET', 'POST'])
@login_required
def sensor_register():
    form = SensorRegisterForm(data={'sensors': [
        {'sensor_type': SensorType.query.get(sensor)}
        for sensor in current_app.config['SENSOR_DEFAULT_SET']
    ]})

    if form.validate_on_submit():
        node = Node(location=SensorLocation(), sensors=[
            Sensor() for _ in form.sensors
        ])

        form.populate_obj(node)
        # node.uid = 'esp8266-' + form.sensor_id.data
        node.uid = form.sensor_board.data + form.sensor_id.data
        node.email = current_user.email

        db.session.add(node)
        db.session.commit()

        flash(_('Sensor succesfuly registered.'), 'success')
        return redirect(url_for('.sensor_list'))

    return render_template('sensor-register.html', node=None, form=form)


@personal.route('/my-sensor/<id>/give', methods=['GET', 'POST'])
@personal.route('/sensors/<id>/transfer', methods=['GET', 'POST'])
@login_required
def sensor_transfer(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    form = SensorGiveForm()
    if form.validate_on_submit():
        node.email = form.email.data.lower()

        msg = Message(_('A fine dust sensor was transferred to you'),
            sender=current_app.config['MAILS_FROM'],
            recipients=[form.email.data.lower()],
            html=render_template('emails/sensor-given.html',
            login_url="%s/login" % (current_app.config['PROJECT_URL']))
        )
        mail.send(msg)
        current_app.logger.info(
            '%s gave node node %s to %s' % (current_user.email, id, form.email.data.lower()))

        db.session.commit()
        return render_template('my-sensor-give-success.html', node=node)
    return render_template('my-sensor-give.html', node=node, form=form)
