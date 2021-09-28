

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread':False},echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation from last year"""
    final_data_point = session.query(measurement.date).order_by(measurement.date.desc()).first()

    last_12_months = dt.date(2017, 8,23) - dt.timedelta(days= 365)

    precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > last_12_months).\
    order_by(measurement.date).all()
    bananas=[    list(el)for el in precipitation]
    return jsonify(bananas)


@app.route("/api/v1.0/stations")
def passengers():
    most_active = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    bananas=[    list(el)for el in most_active]
    return jsonify(bananas)

# TOBS
@app.route("/api/v1.0/tobs")
def tobs():

    most_active = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    
    station_temps = most_active[0][0]

    station_temps = session.query(func.min( measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.station == station_temps).all()
    bananas=[    list(el)for el in station_temps]
    return jsonify(bananas)

if __name__ == '__main__':
    app.run(debug=True)