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


session = Session(engine)

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
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    prcp_data = []
    for date, prcp in results:
        prcp_data.append({date : prcp})

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).distinct().all()
    
    station_data = []
    for name in results:
        station_data.append(name)

    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    
    maxDate = session.query( func.max(Measurement.date).label('maxdate')).all()
    maxDate = list(np.ravel(maxDate))

    maxDate=pd.to_datetime(maxDate[0])

    minDate = maxDate- relativedelta.relativedelta(months=12)

    results = session.query(Measurement.date , Measurement.tobs).filter( Measurement.date >= minDate.date()).all()
    
    tobs_data = []
    for date, tobs in results:
        tobs_data.append([date,tobs])

    return jsonify(tobs_data)




if __name__ == "__main__":
    app.run(debug=True)
