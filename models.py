from extensions import db
from flask_login import UserMixin
from datetime import datetime, time

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class FlightData(db.Model):
    __tablename__ = 'flight_data'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    flight_No_Day = db.Column(db.Integer)
    Operators = db.Column(db.String(100))
    pilot = db.Column(db.String(100))
    flight_date = db.Column(db.Date)
    departure = db.Column(db.String(50))
    overlap = db.Column(db.Float)
    gsd = db.Column(db.String(50))
    aircraft = db.Column(db.String(50))
    navigation_system = db.Column(db.String(50))
    mount = db.Column(db.String(50))
    imu = db.Column(db.String(50))
    camera = db.Column(db.String(50))
    serial_no = db.Column(db.String(50))
    focal_length = db.Column(db.String(50))
    gps_data_logging_time = db.Column(db.Time, nullable=True)
    sun_angle = db.Column(db.String(50))
    internal_pos_data_code = db.Column(db.String(50))
    aperture = db.Column(db.String(50))
    shutter_speed = db.Column(db.String(50))
    iso = db.Column(db.String(50))
    fmc = db.Column(db.String(50))
    ibd = db.Column(db.String(50))
    engine_start = db.Column(db.Time, nullable=True)
    start_movement = db.Column(db.Time, nullable=True)
    take_off = db.Column(db.Time, nullable=True)
    landing = db.Column(db.Time, nullable=True)
    stop_movement = db.Column(db.Time, nullable=True)
    shutdown = db.Column(db.Time, nullable=True)
    weather = db.Column(db.Text)
    remarks = db.Column(db.Text)
    signature = db.Column(db.String(100))

    entries = db.relationship('FlightEntry', backref='flight_data', lazy=True)

class FlightEntry(db.Model):
    __tablename__ = 'flight_entry'
    id = db.Column(db.Integer, primary_key=True)
    flight_data_id = db.Column(db.Integer, db.ForeignKey('flight_data.id'), nullable=False)
    time_of_entry = db.Column(db.Time, nullable=True)
    time_of_end = db.Column(db.Time, nullable=True)
    turning_time = db.Column(db.Integer)
    run = db.Column(db.Integer)
    heading = db.Column(db.Integer)
    dir = db.Column(db.String(10))
    photo_numbers = db.Column(db.String(50))
    qty = db.Column(db.Integer)
    remarks_entry = db.Column(db.Text)
