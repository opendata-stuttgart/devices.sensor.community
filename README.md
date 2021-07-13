# devices.sensor.community
sensor.community self-service registration portal.

## Translations

The files for translation can be found in the folder `translations/<language ISO code>/LC_MESSAGES/`.
Both files flask_security.po and messages.po need to be translated.

There is a free tool to edit and translate these files: https://poedit.net/  

#### Manual translation

Example for translation of a one line text:  
`msgid "Indoor Sensor"` <- english  
`msgstr "Indoor-Sensor"` <- translation  

Example for translation of a text with more than one line:  
(every line has to start and to end with a double quote, first line contains 2 double quote only)  
`msgid ""`  
`"Mark sensor as inactive. No notifications will be sent when sensor goes "`  
`"offline."`  
`msgstr ""`  
`"Markiert den Sensor als inaktiv. Es werden keine Benachrichtigungen mehr "`  
`"versendet, wenn der Sensor keine Daten mehr liefert."`  
  
If you don't have a Github account download the two files via the `Raw` button directly right over their source code. Send us your file with the translation to "tech (at) sensor.community".  

## Configuration file
Default configuration settings (set from `webapp/default_settings.py`) are
suitable for running in non-production Docker environment. If you need to
override any configuration variables, you can create `webapp/config.py` file
based off `webapp/config.py.dist`.

Additionally, when running outside of docker, `.flaskenv` file is required.
Basic development environment file can be copied from `.flaskenv.dist`.

## virtualenv setup

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

### Database intialization

    flask db upgrade

    # Create initial user and roles
    flask users create testing@sensor.community --password password -a
    flask roles create admin
    flask roles add testing@sensor.community admin

### Running

    flask run

## Docker development
To ease up development Docker container and relevant `docker-compose.yml`
project file has been created. Following will start up basic development
environment including MySQL database with "external" schema and redis. Code reloads are active by default.

    docker-compose up

Web application is available on http://localhost:5000/

To create new database migration:

    docker-compose run --rm web flask db migrate -m 'Short change summary'

Flask environment can be overriden by modifying `docker-compose.yml` only.

### Create new language
##### extract text and `lazy_gettext()` functions

    venv/bin/pybabel extract -F ./babel/babel.cfg -k lazy_gettext -o ./babel/messages.pot .

##### update language

    venv/bin/pybabel extract -F ./babel/babel.cfg -k -l -o ./babel/messages.pot .
    venv/bin/pybabel update -i ./babel/messages.pot -d ./translations

##### figure out the country code
    
    venv/bin/pybabel --list-locales

##### create translation files
replace the `country_code` with the language to be translated, e.g. `pt` for Portugese

    venv/bin/pybabel init -i ./babel/messages.pot -d ./translations -l country_code
    venv/bin/pybabel init -i ./babel/flask_security.pot -D flask_security -d ./translations -l country_code

##### translate the strings

 inside `translations/country_code` translate the two created files `message.po` and `flask_security.po`.

##### compile into binary

    venv/bin/pybabel compile -d ./translations/
    venv/bin/pybabel compile -d ./translations/ -D flask_security
    
##### extend the `default_settgings.py`
in line 111 extend the object with the new language. Please add in the previous line a comma at the end.
```python
LANGUAGES = {
    'en': 'English', # add a comma
    'pt': 'Português' # add the new language
}
```

