# encoding: utf-8

"""
CCopyright (c) 2018, Maintainer: David Lackovic
based on Ernesto Ruge https://github.com/ruhrmobil-E/meine-luftdaten/
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os

PROJECT_NAME = "luftdaten"
PROJECT_URL = 'https://meine.luftaten.info'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_VERSION = '0.1.0'
LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'logs'))

DEBUG = False

ADMINS = ['david.lackovic@me.com']

SECRET_KEY = SECURITY_PASSWORD_SALT = 'dummysecret'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

MAIL_DEFAULT_SENDER = SECURITY_EMAIL_SENDER = MAILS_FROM = 'noreply@meine.luftdaten.info'
MAIL_SERVER = 'smtp'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_SUPPRESS_SEND = False

# Default docker mariadb wait_timeout is 600s
SQLALCHEMY_POOL_RECYCLE = 480

# all fields after the scheme are optional, and will default to localhost on port 6379, using database 0.
# redis://:password@hostname:port/db_number
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True

SECURITY_I18N_DIRNAME = os.path.join(PROJECT_ROOT, '..', 'translations')

# Docker defaults
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://devel:devel@mysql/devel'
SQLALCHEMY_BINDS = {
    'external': 'mysql+pymysql://external:external@mysql/external',
}

# Predefined sensor PINs
SENSOR_TYPES = {
    14: '1',
    9: '7',
}

# IDs of default SensorTypes assigned to node
SENSOR_DEFAULT_SET = [
    14, 9,
]

# Update sensor location in-place if it has been modified earlier than N
# seconds ago
SENSOR_LOCATION_UPDATE_INTERVAL = 60 * 60 * 24 * 3  # 3 days

# Default Node.owner_id field value
SENSOR_DEFAULT_OWNER = 1
