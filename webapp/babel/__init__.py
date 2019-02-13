from flask import request,session
from webapp.extensions import babel
from flask import Blueprint


babel_blueprint = Blueprint(
    'babel',
    __name__
)

def create_module(app, **kwargs):
    babel.init_app(app)
    app.register_blueprint(babel_blueprint)

@babel.localeselector
def get_locale():
