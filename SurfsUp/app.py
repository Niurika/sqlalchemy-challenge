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

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date, and prcp"""
    # Query all
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = (session.query(Measurement.date,func.max(Measurement.prcp))
                  .filter(func.strftime('%Y-%m-%d',Measurement.date) >= year_ago_date)
                  .group_by(Measurement.date)
                  .all())

    session.close()

    # Create a dictionary from the row data and append to a list
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        all_prcp.append(prcp_dict)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/tobs")
def tabs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_ago_date=dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query all stations
    results = (session.query(Measurement.date,(Measurement.tobs)).filter(func.strftime(Measurement.date) >= year_ago_date).filter(Measurement.station=='USC00519281').all())
    
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)
    
@app.route("/api/v1.0/<start>")
def start_date(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all
    avg = [Measurement.station,
             func.min(Measurement.tobs),
             func.max(Measurement.tobs),
             func.avg(Measurement.tobs)]
    
    results = (session.query(*avg).filter(Measurement.date >= date)).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all
    avg = [Measurement.station,
             func.min(Measurement.tobs),
             func.max(Measurement.tobs),
             func.avg(Measurement.tobs)]
    
    results = (session.query(*avg).filter(Measurement.date >= start)).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)



if __name__ == '__main__':
    app.run(debug=True)

