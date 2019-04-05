#!/bin/bash
cd /home/meine-luftdaten-info
source venv/bin/activate
venv/bin/gunicorn -c gunicorn.conf wsgi
