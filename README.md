# meine luftdaten
luftdaten.info self-service registration portal.

## Configuration file
To start this project you need to create configuration file in
`webapp/config.py`. Example config (suitable for Docker environment below) is
provided in `webapp/config.py.dist` file. Docker environment uses `LocalConfig`
by default. Also take care of `MAIL_SUPPRESS_SEND` variable during development.

## virtualenv setup
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

### Database intialization
    # Following two commands are not required as of mid-october.
    #python manage.py db init
    #python manage.py db migrate

    python manage.py db upgrade

### Running
    python runserver.py

## Docker development
To ease up development Docker container and relevant `docker-compose.yml`
project file has been created. Following will start up basic development
environment including MySQL database with "external" schema, redis
<s> and celery workers</s>. Code reloads are active by default.

    docker-compose up

Web application is available on http://localhost:5000/

To create new database migration:

    docker-compose run --rm web python3 manage.py db migrate -m 'Short change summary'

### Gulp automatic rebuilds
To start automatic CSS/JS rebuilds on change use this:

    docker-comopose run --rm gulp npm start
