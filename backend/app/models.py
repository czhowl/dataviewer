# encoding: utf-8
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, auth_token_required, http_auth_required
from . import db
from marshmallow import Schema

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

# superuser, admin, author, editor, user
class Role(db.Model, RoleMixin):
	__tablename__ = 'roles'	
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))
	
	def __repr__(self):
		return '<Role %s>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(63))
    current_login_ip = db.Column(db.String(63))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users'))#, lazy='dynamic'))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    #data
    username = db.Column(db.String(64), unique=True)
    lastSync = db.Column(db.DateTime())
    vehicleUse = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    data = db.relationship('Data', backref='data', lazy='dynamic')

    def to_json(self):
        json_user = {
            'username': self.email,
            'lastSync': self.lastSync,
        }
        return json_user
    
    def change_vehicle(self, vehicle_id):
        self.vehicleUse = vehicle_id
    
    def update_sync(self):
        self.lastSync = datetime.utcnow()

    def __repr__(self):
        return '<User-%d %r>' % (self.id, self.email)

class Data(db.Model):
    __tablename__ = 'data'
    # user
    logger_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # data
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    accel_x = db.Column(db.Float)
    accel_y = db.Column(db.Float)
    accel_z = db.Column(db.Float)
    speed = db.Column(db.Float)

    def to_json(self):
        json_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'lat': self.gps_lat,
            'lng': self.gps_lng,
            'accel_x': self.accel_x,
            'accel_y': self.accel_y,
            'accel_z': self.accel_z,
            'speed': self.speed
        }
        return json_data
    
    @staticmethod
    def from_json(json_post):
        data_stream = json_post.get('data')
        print data_stream
        if data_stream is None or data_stream == '':
            raise ('POST does not have data stream')
        data = []
        for d in data_stream:
            print d
            data.append( Data(index=d['index'], timestamp=d['timestamp'], lat=d['lat'], lng=d['lng'], accel_x=d['accel_x'], accel_y=d['accel_y'], accel_z=d['accel_z'], speed=d['speed']) )
        return data
    
class DataSchema(Schema):
    class Meta:
        fields = ('timestamp', 'lat', 'lng', 'accel_z')
    
data_schema = DataSchema(many=True)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    tire_pressure = db.Column(db.Integer)
    make = db.Column(db.String(16))
    model = db.Column(db.String(16))
    year = db.Column(db.Integer)
    logger = db.relationship('User', backref='logger', lazy='dynamic')

    def to_json(self):
        json_vehicle = {
            'weight': self.weight,
            'tire_pressure': self.tire_pressure,
            'make': self.make,
            'model': self.model,
            'year': self.year
        }
        return json_vehicle
    
    @staticmethod
    def from_json(json_post):
        vehicle = json_post.get('vehicle')
        print vehicle
        if vehicle is None or vehicle == '':
            raise ('POST does not have vehicle')
        return Vehicle(weight=vehicle['weight'], tire_pressure=vehicle['tire_pressure'], make=vehicle['make'], model=vehicle['model'], year=vehicle['year'])

class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), primary_key=True, nullable=False)

    @staticmethod
    def clear_A():
        for a in Alembic.query.all():
            print a.version_num
            db.session.delete(a)
        db.session.commit()
        print '======== data in Table: Alembic cleared!'