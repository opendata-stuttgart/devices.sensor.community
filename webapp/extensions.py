from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, email_dispatched
from flask_babelex import Babel, Domain
from flask_security import Security

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
babel = Babel(default_domain=Domain('translations', domain='messages'))
# https://github.com/lingthio/Flask-User/issues/195#issuecomment-352274132
babel.translation_directories = 'translations'
babel.domain = 'webapp'
security = Security()


# When testing without proper mail server set up, set MAIL_SUPPRESS_SEND = True
# config property to enable mail logging.
@email_dispatched.connect
def log_message(message, app):
    if app.config.get('MAIL_SUPPRESS_SEND'):
        app.logger.info('%s\n%s', message.subject, message.body)
