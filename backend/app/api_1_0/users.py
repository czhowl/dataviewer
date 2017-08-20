# encoding: utf-8
import os, json
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User
from flask_jwt import jwt_required, current_identity
from flask_security import auth_token_required, login_required, current_user
from .. import db, basedir

@api.route('/protected')
@auth_token_required
def token_protected():
	return 'you\'re logged in by Token!'

@api.route('/users/<int:id>')
@auth_token_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/relogin')
@login_required
def protected():
    return jsonify({
        'username': current_user.email,
        'authentication_token': current_user.get_auth_token()
    })


