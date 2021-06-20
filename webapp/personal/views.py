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

from flask import (Flask, Blueprint, request, render_template, current_app, flash, url_for, redirect, session)
from flask_login import current_user, login_required
from flask_mail import Message
from flask_babel import lazy_gettext as _
import requests
import dateutil.parser
from datetime import datetime, timedelta
import pytz
import sqlalchemy.exc as exc

from .forms import SensorGiveForm, SensorSettingsForm, SensorRegisterForm, SensorDeleteForm, SensorAddForm
from ..external_data.models import Node, SensorLocation, Sensor, SensorType
from ..common.helpers import get_object_or_404, model_to_dict
from ..extensions import mail, db

personal = Blueprint('personal', __name__)

VALUE_TYPES = {
    'P1': ('µg/m³', _('Fine dust 10 µm')),
    'P2': ('µg/m³', _('Fine dust 2.5 µm')),
    'humidity': ('% RH', _('Humidity')),
    'temperature': ('°C', _('Temperature')),
    'pressure': ('hPa', _('Pressure')),
    'pressure_at_sealevel': ('hPa', _('Pressure at sea level')),
}

SENSOR_TYPES = {
    'PM': _('particulate matter sensor'),
    'TH': _('temperature/humidity sensor'),
    'TP': _('temperature/pressure sensor'),
    'THP': _('temperature/humidity/pressure sensor'),
    'THCO2': _('temperature/humidity/CO₂ ppm sensor'),
    'NOISE': _('noise sensor'),
    'RADIATION': _('radiation sensor'),
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
        if sensor.sensor_type_id == 1:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PPD42NS'
        elif sensor.sensor_type_id == 14:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'SDS011'
        elif sensor.sensor_type_id == 18:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'SDS021'
        elif sensor.sensor_type_id == 21:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PMS1003'
        elif sensor.sensor_type_id == 16:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PMS3003'
        elif sensor.sensor_type_id == 23:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PMS5003'
        elif sensor.sensor_type_id == 24:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PMS6003'
        elif sensor.sensor_type_id == 22:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'PMS7003'
        elif sensor.sensor_type_id == 37:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'SPS30'
        elif sensor.sensor_type_id == 25:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'HPM'
        elif sensor.sensor_type_id == 38:
            sensor.sensor_type_name = SENSOR_TYPES["PM"]
            sensor.sensor_type_id = 'HM3301'
        elif sensor.sensor_type_id == 12:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'DS18S20'
        elif sensor.sensor_type_id == 13:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'DS18B20'
        elif sensor.sensor_type_id == 9:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'DHT22'
        elif sensor.sensor_type_id == 8:
            sensor.sensor_type_name = SENSOR_TYPES["TP"]
            sensor.sensor_type_id = 'BMP180'
        elif sensor.sensor_type_id == 20:
            sensor.sensor_type_name = SENSOR_TYPES["TP"]
            sensor.sensor_type_id = 'BMP280'
        elif sensor.sensor_type_id == 17:
            sensor.sensor_type_name = SENSOR_TYPES["THP"]
            sensor.sensor_type_id = 'BME280'
        elif sensor.sensor_type_id == 19:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'HTU21D'
        elif sensor.sensor_type_id == 4:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT10'
        elif sensor.sensor_type_id == 5:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT11'
        elif sensor.sensor_type_id == 6:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT15'
        elif sensor.sensor_type_id == 26:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT30'
        elif sensor.sensor_type_id == 27:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT31'
        elif sensor.sensor_type_id == 28:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT35'
        elif sensor.sensor_type_id == 39:
            sensor.sensor_type_name = SENSOR_TYPES["TH"]
            sensor.sensor_type_id = 'SHT85'
        elif sensor.sensor_type_id == 40:
            sensor.sensor_type_name = SENSOR_TYPES["THCO2"]
            sensor.sensor_type_id = 'SCD30'
        elif sensor.sensor_type_id == 29:
            sensor.sensor_type_name = SENSOR_TYPES["NOISE"]
            sensor.sensor_type_id = 'DNMS'
        elif sensor.sensor_type_id == 31:
            sensor.sensor_type_name = SENSOR_TYPES["RADIATION"]
            sensor.sensor_type_id = 'SBM-20'
        elif sensor.sensor_type_id == 35:
            sensor.sensor_type_name = SENSOR_TYPES["RADIATION"]
            sensor.sensor_type_id = 'SBM-19'
        elif sensor.sensor_type_id == 36:
            sensor.sensor_type_name = SENSOR_TYPES["RADIATION"]
            sensor.sensor_type_id = 'Si22G'

        try:
            # sensor_request = requests.get('http://api.sensor.community/static/v1/sensor/%s/' % (sensor.id))
            sensor_request = requests.get('http://127.0.0.1/v1/sensor/%s/' % (sensor.id))
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
    form_add_sensor = SensorAddForm()

    if "update" in request.form and form.validate_on_submit():
        print("form is submitted")
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
        print(f'form {form.submit.data}')
        print(f'formAddSensor {form_add_sensor.submit.data}')
        db.session.commit()
        current_app.logger.info('%s updated node %s' % (current_user.email, id))
        flash(_('Settings saved successfully.'), 'success')
        return redirect(url_for('.sensor_list'))

    if "addSensor" in request.form and form_add_sensor.validate():
        print("form_add_sensor is submitted")
        # sensor_fields = [f.short_name for f in form_add_sensor.submit.data]
        # sensor_fields = [f.short_name for f in form_add_sensor.sensors]
        # sensor_fields = [Sensor() for _ in form_add_sensor.sensors]

        try:
            print(f'sensor type: {form_add_sensor.sensor_type.data}')
            print(f'pin: {form_add_sensor.pin.data}')
            st = 20
            sensor = Sensor(sensor_type_id=st, node_id=id, pin=form_add_sensor.pin.data)
            # print(f'---------------------------------')
            db.session.add(sensor)
            db.session.commit()
            print(f'---------------------------------')

            flash(_('Sensor successfully registered.'), 'success')
            return redirect(url_for('.sensor_list'))
        except exc.IntegrityError:
            db.session.rollback()
            flash(_('This sensor ID is already registered.'), 'warning')

    return render_template('my-sensor-settings.html', node=node, form=form, formAddSensor=form_add_sensor,
                           types=current_app.config[
                               'SENSOR_TYPES'])


@personal.route('/sensors/register', methods=['GET', 'POST'])
@login_required
def sensor_register():
    form = SensorRegisterForm(data={'sensors': [
        {'sensor_type': SensorType.query.get(sensor)}
        for sensor in current_app.config['SENSOR_DEFAULT_SET']
    ]})

    if form.validate_on_submit():
        print("register form is submitted")
        node = Node(location=SensorLocation(), sensors=[
            Sensor() for _ in form.sensors
        ])

        form.populate_obj(node)
        # node.uid = 'esp8266-' + form.sensor_id.data
        node.uid = form.sensor_board.data + form.sensor_id.data
        node.email = current_user.email

        try:
            db.session.add(node)
            db.session.commit()

            flash(_('Sensor successfully registered.'), 'success')
            return redirect(url_for('.sensor_list'))
        except exc.IntegrityError:
            db.session.rollback()
            flash(_('This sensor ID is already registered.'), 'warning')

    return render_template('sensor-register.html', node=None, form=form, types=current_app.config['SENSOR_TYPES'])


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
            '%s gave node %s to %s' % (current_user.email, id, form.email.data.lower()))

        db.session.commit()
        return render_template('my-sensor-give-success.html', node=node)
    return render_template('my-sensor-give.html', node=node, form=form)


@personal.route('/my-sensor/<id>/delete', methods=['GET', 'POST'])
@personal.route('/sensors/<id>/delete', methods=['GET', 'POST'])
@login_required
def sensor_delete(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    form = SensorDeleteForm()
    if form.validate_on_submit():
        node.email = 'deleted_' + node.email
        node.inactive = 1

        current_app.logger.info(
            '%s deleted node %s' % (current_user.email, id))

        db.session.commit()
        return render_template('my-sensor-delete-success.html', node=node)
    return render_template('my-sensor-delete.html', node=node, form=form)
