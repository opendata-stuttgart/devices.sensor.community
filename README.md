# meine luftdaten
---

virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

## config erstellen
python manage.py initdb
python manage.py db init

python manage.py db migrate

python manage.py db upgrade

# runserver
python runserver.py