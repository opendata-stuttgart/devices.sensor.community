import pytz
from urllib.parse import quote_plus


def register_global_filters(app):
    @app.template_filter('datetime')
    def template_datetime(datetime, format='medium'):
        if datetime.tzname() == 'UTC':
            datetime = datetime.astimezone(pytz.timezone('Europe/Berlin'))
        datetime = datetime.strftime('%d.%m.%Y, %H:%M:%S')
        return datetime

    @app.template_filter('urlencode')
    def urlencode(data):
        return (quote_plus(data))
