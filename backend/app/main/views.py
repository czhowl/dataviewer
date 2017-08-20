# encoding: utf-8
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, current_user, AnonymousUser, \
    UserMixin, RoleMixin, login_required, auth_token_required, http_auth_required
from flask_security.utils import logout_user
from flask_sqlalchemy import get_debug_queries
from . import main
#from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db, admin
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin._backwards import ObsoleteAttr
from ..models import User, Data, Role, Vehicle,  roles_users
#from ..decorators import admin_required, permission_required
from flask_admin import helpers as admin_helpers

@main.route('/', methods=['GET', 'POST'])
def index():
#    return 'hello'
	return render_template('index.html')

@main.route('/__webpack_hmr')
def npm():
    return redirect('http://localhost:8080/__webpack_hmr')

#@main.route('/protected')
#@login_required
#def protected():
#	print current_user.to_json()
#	print ', '.join(['%s:%s' % item for item in current_user.__dict__.items()])
#	if current_user <> AnonymousUser and not current_user.is_active:
#		logout_user()
#		return "you've been logged out!"	
#	return "protected view!" + str(current_user.to_json())

