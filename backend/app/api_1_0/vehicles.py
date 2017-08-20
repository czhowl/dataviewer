# encoding: utf-8
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Vehicle
from flask_jwt import jwt_required, current_identity
from flask_security import auth_token_required, login_required, current_user
from .. import db

@api.route('/vehicle', methods=['POST'])
@auth_token_required
def new_vehicle():
    email = request.get_json()['email']
    user = User.query.filter_by(email=email).first()
    vehicle = Vehicle.from_json(request.json)
    rsp = []
    v_sql = (Vehicle.query
                 .filter_by(weight=vehicle.weight)
                 .filter_by(tire_pressure=vehicle.tire_pressure)
                 .filter_by(make=vehicle.make)
                 .filter_by(model=vehicle.model)
                 .filter_by(year=vehicle.year).first())
    if v_sql is None:
        db.session.add(vehicle)
        rsp.append(vehicle.to_json())
        db.session.commit()
        user.change_vehicle(vehicle.id)
    else:
        user.change_vehicle(v_sql.id)
        rsp.append(vehicle.to_json())
        db.session.commit()
    
    return jsonify(rsp), 201, \
        {'Location': url_for('api.get_vehicle', id=vehicle.id, _external=True)}

@api.route('/vehicle/')
@auth_token_required
def get_vehicle():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    vehicle_id = user.vehicleUse
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle is not None:
        rsp = vehicle.to_json()
        rsp['lastSync'] = user.lastSync
        return jsonify(rsp)
    else:
        return 'None'