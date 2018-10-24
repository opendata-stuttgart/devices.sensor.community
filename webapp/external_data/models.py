from ..extensions import db
from ..common.helpers import JsonSerializer, get_current_time


class Node(db.Model):
    __tablename__ = 'sensors_node'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time)

    uid = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)

    location_id = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    description_internal = db.Column(db.String)
    email = db.Column(db.String(254))
    height = db.Column(db.Integer)
    sensor_position = db.Column(db.Integer)
    name = db.Column(db.String)
    last_notify = db.Column(db.DateTime)


class Sensor(db.Model):
    __tablename__ = 'sensors_sensor'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time)

    description = db.Column(db.String)

    sensor_type_id = db.Column(db.Integer, nullable=False)
    node_id = db.Column(db.Integer, nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    public = db.Column(db.Boolean, nullable=False)


class SensorLocation(db.Model):
    __tablename__ = 'sensors_sensorlocation'
    __bind_key__ = 'external'

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=get_current_time)
    modified = db.Column(db.DateTime, nullable=False, default=get_current_time)

    location = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)
    indoor = db.Column(db.Boolean, nullable=False)

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
