from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc


import pandas as pd
#import datetime as dt
from dateutil import relativedelta


###DB Connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)



@app.route("/")
def home():
    return( 
        f"Welcome to Surfs Up API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt; <br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )
   


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    
    prcp_data = []
    for date, prcp in results:
        prcp_data.append({date : prcp})

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(Station.station).distinct().all()
    
    station_data = []
    for name in results:
        station_data.append(name)

    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    maxDate = session.query( func.max(Measurement.date).label('maxdate')).all()
    maxDate = list(np.ravel(maxDate))

    maxDate=pd.to_datetime(maxDate[0])

    minDate = maxDate- relativedelta.relativedelta(months=12)

    results = session.query(Measurement.date , Measurement.tobs).filter( Measurement.date >= minDate.date()).all()
    
    tobs_data = []
    for date, tobs in results:
        tobs_data.append([date,tobs])

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start_date>")
def start_only(start_date):
    
    session = Session(engine)
    
    temp_tuple = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    trip_temp = [list(np.ravel(temp_tuple))[0], list(np.ravel(temp_tuple))[1], list(np.ravel(temp_tuple))[2]]

    trip_temp_list = [{'Min temperature': trip_temp[0]}, {'Avg temperature': trip_temp[1]}, {'Max temperature': trip_temp[2]}]
        
    return jsonify(trip_temp_list)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    
    session = Session(engine)
    
    temp_tuple = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    trip_temp = [list(np.ravel(temp_tuple))[0], list(np.ravel(temp_tuple))[1], list(np.ravel(temp_tuple))[2]]

   
    trip_temp_list = [{'Min temperature': trip_temp[0]}, {'Avg temperature': trip_temp[1]}, {'Max temperature': trip_temp[2]}]
        
    #print(trip_temp_list)
    #return jsonify({'a':start_date})
    return jsonify(trip_temp_list)




if __name__ == "__main__":
    app.run(debug=True)
