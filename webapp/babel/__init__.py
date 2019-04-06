from flask import request,session,current_app
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
    if 'lang' in request.args:
        session['lang'] = request.args.get('lang')
    return session.get('lang') or \
        request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())
