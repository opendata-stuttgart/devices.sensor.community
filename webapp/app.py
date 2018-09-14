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

import os
from flask import Flask, request, render_template

from webapp import config as Config
from .common import Response
from .common import constants as COMMON_CONSTANTS
from .common.filter import register_global_filters
from .frontend import frontend
from .personal import personal
from .users import users
from .admin import admin
from .models import User
from .extensions import db, login_manager, csrf, mail, celery

__all__ = ['launch']

DEFAULT_BLUEPRINTS = [
  frontend,
  personal,
  users,
  admin
]

def launch(config=None, app_name=None, blueprints=None):
  """Create a Flask app."""

  if app_name is None:
    app_name = Config.DefaultConfig.PROJECT_NAME
  if blueprints is None:
    blueprints = DEFAULT_BLUEPRINTS

  app = Flask(
    app_name,
    instance_path=COMMON_CONSTANTS.INSTANCE_FOLDER_PATH,
    instance_relative_config=True,
    template_folder='webapp/templates')
  configure_app(app, config)
  configure_hook(app)
  configure_blueprints(app, blueprints)
  configure_extensions(app)
  configure_logging(app)
  configure_filters(app)
  configure_error_handlers(app)
  from .common import filter
  return app

def configure_app(app, config=None):
  """Different ways of configurations."""

  # http://flask.pocoo.org/docs/api/#configuration
  app.config.from_object(Config.DefaultConfig)

  if config:
    app.config.from_object(config)
    return

  # get mode from os environment
  application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
  
  print("Running in %s mode" % application_mode)
  
  app.config.from_object(Config.get_config(application_mode))

def configure_extensions(app):
  # flask-sqlalchemy
  db.init_app(app)
  
  # flask-login

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(id)

  login_manager.setup_app(app)

  @login_manager.unauthorized_handler
  def unauthorized(msg=None):
    return render_template('401.html'), 401
    
  # flask-wtf
  csrf.init_app(app)
  
  # flask-mail
  mail.init_app(app)
  
  #celery
  celery.init_app(app)

def configure_blueprints(app, blueprints):
  for blueprint in blueprints:
    app.register_blueprint(blueprint)

def configure_filters(app):
  register_global_filters(app)
  
def configure_logging(app):
  if not os.path.exists(app.config['LOG_DIR']):
    os.makedirs(app.config['LOG_DIR'])
  
  from logging import INFO, DEBUG, ERROR, handlers, Formatter
  app.logger.setLevel(DEBUG)

  info_log = os.path.join(app.config['LOG_DIR'], 'info.log')
  info_file_handler = handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
  info_file_handler.setLevel(DEBUG)
  info_file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]')
  )

  exception_log = os.path.join(app.config['LOG_DIR'], 'exception.log')
  exception_log_handler = handlers.RotatingFileHandler(exception_log, maxBytes=100000, backupCount=10)
  exception_log_handler.setLevel(ERROR)
  exception_log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s ')
  )
  app.logger.addHandler(info_file_handler)
  app.logger.addHandler(exception_log_handler)

def configure_hook(app):
  @app.before_request
  def before_request():
    pass

def configure_error_handlers(app):
  pass
"""
  @app.errorhandler(500)
  def server_error_page(error):
    return Response.make_error_resp(msg=str(error), code=500)  

  @app.errorhandler(422)
  def semantic_error(error):
    return Response.make_error_resp(msg=str(error.description), code=422)

  @app.errorhandler(404)
  def page_not_found(error):
    return Response.make_error_resp(msg=str(error.description), code=404)

  @app.errorhandler(403)
  def page_forbidden(error):
    return Response.make_error_resp(msg=str(error.description), code=403)

  @app.errorhandler(400)
  def page_bad_request(error):
    return Response.make_error_resp(msg=str(error.description), code=400)
"""