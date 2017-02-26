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

from flask import (Flask, Blueprint, render_template, current_app, request, flash, url_for, redirect, session, abort, jsonify, send_from_directory)
from flask_login import current_user, login_required
from .PersonalForms import *
from ..external_data import ExternalNodes

personal = Blueprint('personal', __name__)

@personal.route('/meine-luftdaten')
@login_required
def meine_luftdaten():
  return render_template('meine-luftdaten.html')

@personal.route('/meine-einstellungen')
@login_required
def meine_einstellungen():
  return render_template('meine-einstellungen.html')

@personal.route('/meine-sensoren')
@login_required
def meine_sensoren():
  external_nodes = ExternalNodes()
  return render_template('meine-sensoren.html', nodes=external_nodes.get_nodes_by_email(current_user.email))

@personal.route('/mein-sensor/<id>/daten')
@login_required
def mein_sensor_daten(id):
  external_nodes = ExternalNodes()
  node = external_nodes.get_sensors(id, current_user.email)
  if node == False:
    abort(403)
  return render_template('mein-sensor-daten.html', node=node)

@personal.route('/mein-sensor/<id>/einstellungen', methods=['GET', 'POST'])
@login_required
def mein_sensor_einstellungen(id):
  external_nodes = ExternalNodes()
  node = external_nodes.get_node_by_id(id, current_user.email)
  if node == False:
    abort(403)
  form = SensorSettingsForm()
  if form.validate_on_submit():
    external_nodes.update_meta(id, current_user.email)
    flash('Einstellungen erfolgreich gespeichert.', 'success')
    return redirect('/meine-sensoren')
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
    if form.email.data == current_user.email:
      flash('Sie können den Sensor nicht an sich selbst übergeben.', 'error')
    else:
      if external_nodes.update_email(id, current_user.email, form.email.data):
        return render_template('mein-sensor-give-success.html', node=node)
      else:
        flash('Ein serverseitiger Fehler ist aufgetreten. Bitte versuchen Sie es später noch einmal.')
  return render_template('mein-sensor-give.html', node=node, form=form)