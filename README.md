# meine luftdaten
luftdaten.info self-service registration portal.

## Configuration file
To start this project you need to create configuration file in
`webapp/config.py`. Example config (suitable for Docker environment below) is
provided in `webapp/config.py.dist` file. Docker environment uses `LocalConfig`
by default. Also take care of `MAIL_SUPPRESS_SEND` variable during development.

Additionally, when running outside of docker, `.flaskenv` file is required.
Basic development environment file can be copied from `.flaskenv.dist`.

## virtualenv setup
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

### Database intialization

    flask db upgrade

    # Create initial user and roles
    flask users create testing@luftdaten.info --password password -a
    flask roles create admin
    flask roles add testing@luftdaten.info admin

### Running

    flask run

## Docker development
To ease up development Docker container and relevant `docker-compose.yml`
project file has been created. Following will start up basic development
environment including MySQL database with "external" schema, redis
<s> and celery workers</s>. Code reloads are active by default.

    docker-compose up

Web application is available on http://localhost:5000/

To create new database migration:

    docker-compose run --rm web flask db migrate -m 'Short change summary'

Flask environment can be overriden by modifying `docker-compose.yml` only.

### Gulp automatic rebuilds
To start automatic CSS/JS rebuilds on change use this:

    docker-compose run --rm gulp npm start




### Create new langauge

extract text and lazy_gettext() functions

    pybabel extract -F ./babel/babel.cfg -k lazy_gettext -o ./babel/messages.pot .
    
update langauge

    pybabel extract -F ./babel/babel.cfg -k _l -o ./babel/messages.pot .    
    pybabel update -i ./babel/messages.pot -d ./translations

create translated language

    pybabel init -i ./babel/messages.pot -d ./translations -l country_code


compile into binary

    pybabel compile -d ./translations/