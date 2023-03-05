#!/bin/bash
cd /home/devices.sensor.community
source venv/bin/activate
venv/bin/gunicorn -c gunicorn.conf wsgi
