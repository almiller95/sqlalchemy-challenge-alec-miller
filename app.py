# 1. import Flask
from flask import Flask, jsonify

import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome! Check out some Climate Stats below!<br/>"
        f"Available Data:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def prcp():
    print("Server received request for 'About' page...")

    # create a session
    session = Session(engine)

    # Query date and prcp value
    results_prcp = session.query(Measurement.date,Measurement.prcp).all()

    # closing session
    session.close()

    # Create a dictionary from the row data and append to a list of all dates
    all_observation_dates = []
    for date, prcp in results_prcp:
            observation_date_dict = {}
            observation_date_dict["date"] = date
            observation_date_dict["prcp"] = prcp
            all_observation_dates.append(observation_date_dict)
    return (jsonify(all_observation_dates))

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'About' page...")

    # create a session
    session = Session(engine)

    # Query date and prcp value
    results_station = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    # closing session
    session.close()
    
    stations = []
    for id, station, name, latitude, longitude, elevation in results_station:
            station_dict = {}
            station_dict["id"] = id
            station_dict["station"] = station
            station_dict["name"] = name
            station_dict["latitude"] = latitude
            station_dict["longitude"] = longitude
            station_dict["elevation"] = elevation
            stations.append(station_dict)
    return (jsonify(stations))
    # all_stations = list(np.ravel(results_station))
    # return jsonify(all_stations)


# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'About' page...")

    # create a session
    session = Session(engine)

    # running a query
    most_recent_waihee_dt = dt.datetime(2017, 8, 18)
    year_ago_waihee = most_recent_waihee_dt - dt.timedelta(days=365)

    results_tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= year_ago_waihee).filter(Measurement.station == 'USC00519281').all()

    # closing session
    session.close()

    tobs_last = []
    for date, tobs in results_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_last.append(tobs_dict)
    tobs_j = jsonify(tobs_last)
    
    return tobs_j
    #x

@app.route("/api/v1.0/<start>")
def start(start_date):
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page! This is where I will talk about myself"

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page! This is where I will talk about myself"

if __name__ == "__main__":
    app.run(debug=True)