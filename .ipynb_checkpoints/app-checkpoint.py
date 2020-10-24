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

# Route to Precipitation
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
    
if __name__ == "__main__":
    app.run(debug=True)
    