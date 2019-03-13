import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
   return ( 
       f"Welcome to the Hawaii Climate Analysis API Webpage!!!<br/>"
       '\n'
       f"Available Routes:<br/>"
       '\n'
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/temp/start_date<br/>"
       f"/api/v1.0/temp/start_date/end_date<br/>"
       f"/api/v1.0/temp/enter_date<br/>"
   )
@app.route("/api/v1.0/precipitation")
def precipitation():

    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precip_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()

    precip = {date: prcp for date, prcp in precip_results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

   station_results = session.query(Station.station).all()

   stations = list(np.ravel(station_results))
   return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

   start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
   tobs_results = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.date >= start_date).all()

   temp = list(np.ravel(tobs_results))
   return jsonify(temp)

@app.route("/api/v1.0/temp/<start_date>")

def temp_start(start_date):

    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    mam_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
    
    mam_temp_start = list(np.ravel(mam_temp_results))
    return jsonify(mam_temp_start)

@app.route("/api/v1.0/temp/<start_date>/<end_date>")

def temp_daterange(start_date,end_date):

    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    mam_temp_dr_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    mam_temp_start_end = list(np.ravel(mam_temp_dr_results))
    return jsonify(mam_temp_start_end)

@app.route("/api/v1.0/temp/<enter_date>")

def temp_date(enter_date):

    """TMIN, TAVG, and TMAX for a specific date.
    Args:
        enter_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """
    mam_temp_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date == enter_date).all()
    
    mam_temp_date = list(np.ravel(mam_temp_date_results))
    return jsonify(mam_temp_date)

if __name__ == '__main__':
   app.run()