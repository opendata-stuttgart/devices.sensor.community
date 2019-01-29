from flask import has_request_context, session
from flask import (current_app, request, session)
from flask_babel import Babel
from flask import current_app

app = current_app

babel = Babel()

def create_module(app, **kwargs):
    babel.init_app(app)
    from .controllers import babel_blueprint
    app.register_blueprint(babel_blueprint)

@babel.localeselector
def get_locale():
    #     # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     return user.locale
    # # otherwise try to guess the language from the user accept
    # # header the browser transmits.  We support de/fr/en in this
    # # example.  The best match wins.
    # return request.accept_languages.best_match(['en', 'de'])
    if has_request_context():
        locale = session.get('locale')
        if locale:
            return locale
        session['locale'] = 'en'
        return session['locale']



# @babel.timezoneselector
# def get_timezone():
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.timezone




