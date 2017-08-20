import os
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Data, data_schema
from flask_security import auth_token_required, login_required, current_user
from .. import db, basedir
from werkzeug.utils import secure_filename
from datetime import datetime
import dataProcess


@api.route('/upload-data', methods=['POST'])
@auth_token_required
def upload_file():
    user = User.query.filter_by(email=request.form['email']).first()
    for file in request.files.values():
        filename = secure_filename(str(user.id)+' '+str(datetime.utcnow()))
        filepath = os.path.join(basedir,'rawData', filename)
        file.save(filepath)
        dataProcess.import_csv(filepath)
    user.update_sync()
    return jsonify(user.to_json())

@api.route('/get-data', methods=['GET'])
@auth_token_required
def get_data():
    resolution = 100
    print datetime.now().time()
    user = User.query.filter_by(email=request.args.get('email')).first()
    data = Data.query.filter_by(logger_id=user.id).all()
    if data:
        rsp = data_schema.dump(data[0:len(data):len(data)/resolution])
        print datetime.now().time()
        return jsonify(rsp.data)
    else:
        return jsonify('none')
    #standard deviation
    #frequency
    #timerange
    #gps range
    #raw data range