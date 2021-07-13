from flask_babel import get_locale


def register_context_processor(app):
    @app.context_processor
    def inject_conf_var():
        return {
            'get_locale': get_locale,
        }
