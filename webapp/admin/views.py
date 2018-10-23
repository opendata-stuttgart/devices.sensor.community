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
from .forms import *
from .helpers import *
from ..extensions import celery

admin = Blueprint('admin', __name__)


@admin.route('/admin/sensor-import', methods=['GET', 'POST'])
@login_required
def admin_sensor_import():
    if not current_user.has_role('Administrator'):
        abort(403)
    form = SensorImportForm()
    if form.validate_on_submit():
        new_sensors = form.data_field.data.replace("\r", "").split("\n")
        # print("New sensor:", new_sensors)
        # Todo implement .delay() function
        sensor_import_worker(new_sensors)
        return redirect('/admin/sensor-import-status')
    return render_template('sensor-import.html', form=form)


@admin.route('/admin/sensor-import-status')
@login_required
def admin_sensor_import_status():
    if not current_user.has_role('Administrator'):
        abort(403)
    task_items_raw = celery.control.inspect().active()
    print("Task items:", task_items_raw)
    task_items = []
    if task_items_raw:
        task_items_raw = next(iter(task_items_raw.values()))
        for task_item_raw in task_items_raw:
            if task_item_raw['type'] == 'webapp.admin.AdminHelper.sensor_import_worker':
                task_items.append({
                    'first_line': task_item_raw['args'] if len(task_item_raw['args']) < 30 else task_item_raw['args'][
                                                                                                0:30] + '...',
                    'id': task_item_raw['id']
                })
    return render_template('sensor-import-status.html', task_items=task_items)
