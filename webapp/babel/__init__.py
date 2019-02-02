from flask import request,session
from flask_babel import Babel
from flask import Blueprint

babel = Babel()

babel_blueprint = Blueprint(
    'babel',
    __name__
)

def create_module(app, **kwargs):
    babel.init_app(app)
    app.register_blueprint(babel_blueprint)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en','de'])