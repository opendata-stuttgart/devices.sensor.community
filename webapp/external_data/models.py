from flask import current_app
from sqlalchemy.orm import backref

from ..extensions import db
from ..common.helpers import JsonSerializer, get_current_time


class Node(db.Model):
    __tablename__ = 'sensors_node'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time,
                         onupdate=get_current_time)

    uid = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('sensors_sensorlocation.id'), nullable=False)
    location = db.relationship('SensorLocation')

    owner_id = db.Column(db.Integer, nullable=False,
                         default=lambda: current_app.config['SENSOR_DEFAULT_OWNER'])
    description_internal = db.Column(db.String)

    email = db.Column(db.String(254))
    owner = db.relationship('User', primaryjoin='User.email == Node.email',
                            foreign_keys='Node.email', remote_side='User.email',
                            backref=backref('nodes', lazy='dynamic'), lazy=True)

    height = db.Column(db.Integer)
    sensor_position = db.Column(db.Integer)
    name = db.Column(db.String)
    last_notify = db.Column(db.DateTime)

    indoor = db.Column(db.Boolean, nullable=False, default=False)
    inactive = db.Column(db.Boolean, nullable=False, default=False)
    exact_location = db.Column(db.Boolean, nullable=False, default=False)


class Sensor(db.Model):
    __tablename__ = 'sensors_sensor'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time,
                         onupdate=get_current_time)

    description = db.Column(db.String)

    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensors_sensortype.id'), nullable=False)
    sensor_type = db.relationship('SensorType')

    node_id = db.Column(db.Integer, db.ForeignKey('sensors_node.id'), nullable=False)
    node = db.relationship('Node', backref='sensors')

    pin = db.Column(db.String(10), nullable=False)
    public = db.Column(db.Boolean, nullable=False, default=False)


class SensorType(db.Model):
    __tablename__ = 'sensors_sensortype'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time,
                         onupdate=get_current_time)

    uid = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    manufacturer = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(10000))

    def __str__(self):
        return '{0.name}'.format(self)


class SensorLocation(db.Model):
    __tablename__ = 'sensors_sensorlocation'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time,
                         onupdate=get_current_time)

    location = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False, default=get_current_time)
    description = db.Column(db.String)
    indoor = db.Column(db.Boolean, nullable=False, default=False)

    owner_id = db.Column(db.Integer)

    latitude = db.Column(db.Numeric(14, 11))
    longitude = db.Column(db.Numeric(14, 11))
    altitude = db.Column(db.Numeric(14, 8))

    industry_in_area = db.Column(db.Integer)
    oven_in_area = db.Column(db.Integer)
    traffic_in_area = db.Column(db.Integer)

    street_name = db.Column(db.String)
    street_number = db.Column(db.String)
    postalcode = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
