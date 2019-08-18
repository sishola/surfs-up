from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc


###DB Connection
engine = create_engine("sqlite:///hawaii.sqlite")

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
    
    #session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    prcp_data = []
    for date, prcp in results:
        #prcp_dict = {date : prcp}
        prcp_data.append({date : prcp})

    return jsonify(prcp_data)






if __name__ == "__main__":
    app.run(debug=True)
