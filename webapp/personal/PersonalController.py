# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask import (Flask, Blueprint, render_template, current_app, request, flash, url_for, redirect, session, abort, jsonify, send_from_directory)
from flask_login import current_user, login_required
from .PersonalForms import *
from ..external_data import ExternalNodes
from ..extensions import mail
from flask_mail import Message
import requests
import dateutil.parser
import pytz

personal = Blueprint('personal', __name__)

@personal.route('/meine-luftdaten')
@login_required
def meine_luftdaten():
  return render_template('meine-luftdaten.html')

@personal.route('/meine-sensoren')
@login_required
def meine_sensoren():
  external_nodes = ExternalNodes()
  return render_template('meine-sensoren.html', nodes=external_nodes.get_nodes_by_email(current_user.email))

@personal.route('/mein-sensor/<id>/daten')
@login_required
def mein_sensor_daten(id):
  external_nodes = ExternalNodes()
  node = external_nodes.get_node_by_id(id, current_user.email)
  sensors = external_nodes.get_sensors(id, current_user.email)
  for sensor in sensors:
    if sensor['sensor_type_id'] == 14:
      sensor['sensor_type_name'] = 'Feinstaub-Sensor SDS011'
    elif sensor['sensor_type_id'] == 9:
      sensor['sensor_type_name'] = 'Feuchtigkeits- und Temperatur-Sensor DHT22'
    sensor_request = requests.get('http://api.luftdaten.info/static/v1/sensor/%s/' % (sensor['id']))
    if sensor_request.status_code == 200:
      sensor_request = sensor_request.json()
      if sensor_request:
        sensor['data'] = sensor_request[0]
        if sensor['data']['timestamp']:
          sensor['data']['timestamp'] = dateutil.parser.parse(sensor['data']['timestamp']).replace(tzinfo=pytz.UTC)
        if sensor['data']['sensordatavalues']:
          for sensor_value in sensor['data']['sensordatavalues']:
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
            elif sensor_value['value_type'] == 'P2':
              sensor_value['value_type_unit'] = ''
              sensor_value['value_type_name'] = 'Unbekannte Größe'
  if node == False:
    abort(403)
  return render_template('mein-sensor-daten.html', node=node, sensors=sensors)

@personal.route('/mein-sensor/<id>/einstellungen', methods=['GET', 'POST'])
@login_required
def mein_sensor_einstellungen(id):
  external_nodes = ExternalNodes()
  node = external_nodes.get_node_by_id(id, current_user.email)
  if node == -1:
    abort(403)
  form = SensorSettingsForm()
  if request.method == 'GET':
    if 'name' in node:
      form.name.data = node['name']
    if 'description' in node:
      form.description.data = node['description']
    if 'height' in node:
      form.height.data = node['height']
    if 'lat' in node:
      form.lat.data = node['lat']
    if 'lon' in node:
      form.lon.data = node['lon']
    if 'street_name' in node:
      form.street_name.data = node['street_name']
    if 'street_number' in node:
      form.street_number.data = node['street_number']
    if 'postalcode' in node:
      form.postalcode.data = node['postalcode']
    if 'city' in node:
      form.city.data = node['city']
    if 'country' in node:
      form.country.data = node['country']
    if 'traffic_in_area' in node:
      form.traffic_in_area.data = node['traffic_in_area']
    if 'oven_in_area' in node:
      form.oven_in_area.data = node['oven_in_area']
    if 'industry_in_area' in node:
      form.industry_in_area.data = node['industry_in_area']
    if 'sensor_position' in node:
      form.sensor_position.data = node['sensor_position']
  if form.validate_on_submit():
    if external_nodes.update_node_meta(id,
                                  current_user.email,
                                  name=form.name.data,
                                  description=form.description.data,
                                  height=form.height.data,
                                  lat=form.lat.data,
                                  lon=form.lon.data,
                                  street_name=form.street_name.data,
                                  street_number=form.street_number.data,
                                  postalcode=form.postalcode.data,
                                  city=form.city.data,
                                  country=form.country.data,
                                  traffic_in_area=form.traffic_in_area.data,
                                  oven_in_area=form.oven_in_area.data,
                                  industry_in_area=form.industry_in_area.data,
                                  sensor_position=form.sensor_position.data
                                  ) != -1:
      current_app.logger.info('%s updated node %s' % (current_user.email, id))
      flash('Einstellungen erfolgreich gespeichert.', 'success')
      return redirect('/meine-sensoren')
    else:
      flash('Ein serverseitiger Fehler ist aufgetreten. Bitte versuchen Sie es später noch einmal.', 'danger')
  return render_template('mein-sensor-einstellungen.html', node=node, form=form)

@personal.route('/mein-sensor/<id>/give', methods=['GET', 'POST'])
@login_required
def mein_sensor_give(id):
  external_nodes = ExternalNodes()
  node = external_nodes.get_node_by_id(id, current_user.email)
  if node == False:
    abort(403)
  form = SensorGiveForm()
  if form.validate_on_submit():
    if form.email.data.lower() == current_user.email:
      flash('Sie können den Sensor nicht an sich selbst übergeben.', 'danger')
    else:
      if external_nodes.update_email(id, current_user.email, form.email.data.lower()) != -1:
        msg = Message(
          "Ein Feinstaubsensor wurde Ihnen übertragen",
          sender = current_app.config['MAILS_FROM'],
          recipients = [  form.email.data.lower() ],
          body = render_template('emails/sensor-given.txt', login_url="%s/login" % (current_app.config['PROJECT_URL']))
        )
        mail.send(msg)
        current_app.logger.info('%s gave node node %s to %s' % (current_user.email, id, form.email.data.lower()))
        return render_template('mein-sensor-give-success.html', node=node)
      else:
        flash('Ein serverseitiger Fehler ist aufgetreten. Bitte versuchen Sie es später noch einmal.', 'danger')
  return render_template('mein-sensor-give.html', node=node, form=form)

