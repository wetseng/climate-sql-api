import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# reflect an existing database into a new model
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# /
# Home page.
# List all routes that are available.

@app.route("/")
def home():

    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results =  session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    results_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        results_list.append(precipitation_dict)

    return jsonify(results_list)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results =  session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    results_list = list(np.ravel(results))

    # results_list = []
    # for stations in results:
    #     stations_dict={}
    #     stations_dict['stations'] = stations
    #     results_list.append(stations_dict)

    return jsonify(results_list)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_id = 'USC00519281'

    date_begin = dt.date(2017,8,23) - dt.timedelta(days=365)


    results =  session.query(Measurement.tobs)\
                .filter_by(station = station_id)\
                .filter(Measurement.date >= date_begin)\
                .all()

    session.close()

    results_list = list(np.ravel(results))

    return jsonify(results_list)


# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def tobs_start(start):

    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .first()
    tmax = session.query(func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .first()
    tavg = session.query(func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .first()

    session.close()

    results_list = [tmin]

    return jsonify(results_list)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):

    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .first()
    tmax = session.query(func.max(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .first()
    tavg = session.query(func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .first()


    session.close()

    results_list = [tmin]

    return jsonify(results_list)


if __name__ == "__main__":
    app.run(debug=True)






