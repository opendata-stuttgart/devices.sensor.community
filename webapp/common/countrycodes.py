import pycountry
from flask_babelex import Domain

domain = Domain(pycountry.LOCALES_DIR, domain='iso3166')

country_codes = [(c.alpha_2, domain.lazy_gettext(c.name)) for c in pycountry.countries]
country_codes.insert(0,('--','--'))
