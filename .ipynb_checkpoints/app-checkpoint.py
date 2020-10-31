# Import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt


# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# Mapping measurement class
Measurement = Base.classes.measurement
# Mapping station class
Station = Base.classes.station


# Flask app setup
app = Flask(__name__)


# Create all Flask routes

# Route to Homepage
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaiian Climate API!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: <a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"Stations: <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"Temperature Observations: <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"Temperature Analysis from Start Date: <a href='/api/v1.0/yyyy-mm-dd'>/api/v1.0/yyyy-mm-dd</a><br/>"
        f"Temperature Analysis from Start to End Dates: <a href='/api/v1.0/yyyy-mm-dd/yyyy-mm-dd'>/api/v1.0/yyyy-mm-dd/yyyy-mm-dd</a><br/>"
    )

# Route to Precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
# Session link to database, and query
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()
# Convert to list and jsonify
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = f"{prcp} mm"
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)
    
# Route to Stations
@app.route("/api/v1.0/stations")
def stations():
# Session link to database and query
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
# Convert to list to jsonify 
    stations_list = []
    for station, name, latitude, longitude, elevation in results:
        stations_dict = {}
        stations_dict["Station"] = station
        stations_dict["Name"] = name
        stations_dict["Latitude"] = latitude
        stations_dict["Longitude"] = longitude 
        stations_dict["Elevation"] = elevation
        stations_list.append(stations_dict)
    return jsonify(stations_list)


# Route to Temperature Observation Bias data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year = dt.date (2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year).order_by(Measurement.date.desc()).all()
    session.close()
# Convert to list to jsonify 
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["TOBS"] = f"{tobs} F"
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)


# Route for Temperatures with Start date
@app.route("/api/v1.0/<start>")
def temp_start(start):
# Session link to database, and query 
    session = Session(engine)
    start = dt.datetime(2015, 12, 3)
    results = session.query(func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).all()
    session.close()
# Convert to list to jsonify
    temp_start_list = []
    for min, avg, max in results:
        temp_start_dict = {}
        temp_start_dict["TMIN"] = min
        temp_start_dict["TAVG"] = avg
        temp_start_dict["TMAX"] = max
        temp_start_list.append(temp_start_dict)
    return jsonify(temp_start_list)


# Route for Temperatures with Start and End date 
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
# Session link to database, and query 
    session = Session(engine)
    start = dt.datetime(2011, 12, 15)
    end = dt.datetime(2015, 8, 23)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
# Convert to list to jsonify
    temp_start_end_list = []
    for min, avg, max in results:
        temp_start_end_dict = {}
        temp_start_end_dict["Min"] = min
        temp_start_end_dict["Average"] = avg
        temp_start_end_dict["Max"] = max
        temp_start_end_list.append(temp_start_end_dict)
    return jsonify(temp_start_end_list)


if __name__ == "__main__":
    app.run(debug=True)
    