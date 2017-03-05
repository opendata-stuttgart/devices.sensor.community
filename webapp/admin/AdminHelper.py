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
from ..external_data import ExternalNodes
from ..extensions import celery, mail
from flask_celery import single_instance
import time
from flask_mail import Message

@celery.task(bind=True)
@single_instance
def sensor_import_worker(new_sensors):
  external_nodes = ExternalNodes()
  for new_sensor in new_sensors:
    new_sensor = new_sensor.split(' ')
    if len(new_sensor) > 0:
      sensor_id = new_sensor[0]
      sensor_email = None
      if len(new_sensor) > 1:
        sensor_email = new_sensor[1].lower()
      save_data_status = external_nodes.insert_new_node_with_sensors(
        uid='esp8266-' + sensor_id,
        email=sensor_email
      )
      if save_data_status == -1:
        msg = Message(
          "Kritischer Datenbankfehler",
          sender = current_app.config['MAILS_FROM'],
          recipients = [ current_app.config['MAILS_FROM'] ],
          body = "Kritischer Datenbankfehler beim luftdaten.org Import"
        )
        mail.send(msg)
      if sensor_email and save_data_status != -1:
        msg = Message(
          "Ihr Feinstaubsensor wurde registriert",
          sender = current_app.config['MAILS_FROM'],
          recipients = [  sensor_email ],
          body = render_template('emails/sensor-registered.txt', login_url="%s/login" % (current_app.config['PROJECT_URL']))
        )
        mail.send(msg)
      