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
The default configuration settings are set in`webapp/default_settings.py`. If you need to override any configuration variables, you can create `webapp/config.py` file based off `webapp/config.py.dist`.

Additionally, `.flaskenv` file is required. Basic development environment file can be copied from `.flaskenv.dist`.

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

## Compile CSS
install node packages

```bash
npm install
```

The project uses [Tailwind CSS](https://tailwindcss.com/), go and check out the [documentation](https://tailwindcss.com/docs) to get started.

```
npm run watch
```

To get ready for production compile the final version

```bash
npm run build
```

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
    
##### extend the `default_settings.py`
in line 111 extend the object with the new language. Please add in the previous line a comma at the end.
```python
LANGUAGES = {
    'en': 'English', # add a comma
    'pt': 'Português' # add the new language
}
```

