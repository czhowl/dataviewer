import os
from .. import db
from ..models import Data
from flask_security import current_user
import pandas as pd
import numpy as np
from datetime import datetime

def import_csv(path):
    print 'start parsing data: ' + str(datetime.now())
    data = pd.read_csv(path,
                       names=['index','date','time','lat','lng','accel_x','accel_y','accel_z','speed'], 
                       usecols=['date','time','lat','lng','accel_x','accel_y','accel_z','speed'],
                       dtype=[('index',np.uint64),('date',object),('time',object),('gps_lat',np.float64),('gps_lng',np.float64),('accel_x',np.float32),('accel_y',np.float32),('accel_z',np.float32),('speed',np.float32)], 
                       parse_dates={'timestamp':[0,1]})
    #for updated data form
#    data = pd.read_csv(path, index_col=0, 
#                       names=['index','timestamp','gps_lat','accel_x','gps_lng','accel_y','accel_z','speed'], 
#                       dtype=[('index',np.uint64),('timestamp',object),('gps_lat',np.float64),('gps_lng',np.float64),('accel_x',np.float32),('accel_y',np.float32),('accel_z',np.float32),('speed',np.float32)], 
#                       parse_dates='timestamp')
    data['logger_id'] = current_user.id
    print 'start writing data: ' + str(datetime.now())
    listToWrite = data.to_dict(orient='records')
    #db.session.bulk_insert_mappings(Data, listToWrite)
    db.session.execute(Data.__table__.insert(),listToWrite)
    db.session.commit()
    print 'done: ' + str(datetime.now())
    os.remove(path)
    
    
    #TODO
    #validating files
