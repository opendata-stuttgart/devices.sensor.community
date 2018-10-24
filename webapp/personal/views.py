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

from flask import (Flask, Blueprint, render_template, current_app, request, flash, url_for, redirect, session, abort,
                   jsonify, send_from_directory)
from flask_login import current_user, login_required
from flask_mail import Message
import requests
import dateutil.parser
import pytz
import json

from .forms import *
from ..external_data.models import Node
from ..common.helpers import get_object_or_404
from ..extensions import mail, db

personal = Blueprint('personal', __name__)


@personal.route('/meine-luftdaten')
@personal.route('/dashboard')
@login_required
def dashboard():
    return render_template('meine-luftdaten.html')


@personal.route('/meine-sensoren')
@personal.route('/sensors')
@login_required
def sensor_list():
    return render_template('meine-sensoren.html', nodes=current_user.nodes)


@personal.route('/mein-sensor/<id>/daten')
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
                if sensor_value['value_type'] == 'P1':
                    sensor_value['value_type_name'] = 'Feinstaub 10 µm'
                    sensor_value['value_type_unit'] = 'µg'
                elif sensor_value['value_type'] == 'P2':
                    sensor_value['value_type_name'] = 'Feinstaub 2,5 µm'
                    sensor_value['value_type_unit'] = 'µg'
                elif sensor_value['value_type'] == 'humidity':
                    sensor_value['value_type_unit'] = '%'
                    sensor_value['value_type_name'] = 'Luftfeuchtigkeit'
                elif sensor_value['value_type'] == 'temperature':
                    sensor_value['value_type_unit'] = '°C'
                    sensor_value['value_type_name'] = 'Temperatur'
                else:
                    sensor_value['value_type_unit'] = ''
                    sensor_value['value_type_name'] = sensor_value['value_type']
    return render_template('mein-sensor-daten.html', node=node, sensors=sensors)


@personal.route('/mein-sensor/<id>/einstellungen', methods=['GET', 'POST'])
@personal.route('/sensors/<id>/settings', methods=['GET', 'POST'])
@login_required
def sensor_settings(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    form = SensorSettingsForm(obj=node)

    if form.validate_on_submit():
        form.populate_obj(node)
        db.session.commit()
        current_app.logger.info('%s updated node %s' % (current_user.email, id))
        flash('Einstellungen erfolgreich gespeichert.', 'success')
        return redirect(url_for('.sensor_list'))

    return render_template('mein-sensor-einstellungen.html', node=node, form=form)


@personal.route('/mein-sensor/<id>/give', methods=['GET', 'POST'])
@personal.route('/sensors/<id>/transfer', methods=['GET', 'POST'])
@login_required
def sensor_transfer(id):
    node = get_object_or_404(Node, Node.id == id, Node.email == current_user.email)
    form = SensorGiveForm()
    if form.validate_on_submit():
        if form.email.data.lower() == current_user.email:
            flash('Sie können den Sensor nicht an sich selbst übergeben.', 'danger')
        else:
            node.email = form.email.data.lower()

            msg = Message(
                "Ein Feinstaubsensor wurde Ihnen übertragen",
                sender=current_app.config['MAILS_FROM'],
                recipients=[form.email.data.lower()],
                body=render_template('emails/sensor-given.txt',
                                        login_url="%s/login" % (current_app.config['PROJECT_URL']))
            )
            mail.send(msg)
            current_app.logger.info(
                '%s gave node node %s to %s' % (current_user.email, id, form.email.data.lower()))

            db.session.commit()
            return render_template('mein-sensor-give-success.html', node=node)
    return render_template('mein-sensor-give.html', node=node, form=form)
