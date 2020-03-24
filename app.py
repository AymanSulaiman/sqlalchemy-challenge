import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database stuff that needs to be set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def index():
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
    )

@app.route("/api/v1.0/precipitation")
#  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#  Return the JSON representation of your dictionary.
def precipitation():
    session = Session(engine)
    results_date_prcp = session.query(
        Measurement.date, 
        Measurement.prcp
    ).all()
    
    session.close()
    dates_and_pcrp = []
    for date, pcrp in results_date_prcp:
        date_pcrp_dict = {}
        date_pcrp_dict["date"] = date
        date_pcrp_dict["pcrp"] = pcrp
        dates_and_pcrp.append(date_pcrp_dict)

    return jsonify(dates_and_pcrp)

@app.route("/api/v1.0/stations")
#  Return a JSON list of stations from the dataset.
def stations():
    session = Session(engine)
    results_stations = session.query(
        Station.id,
        Station.name
    ).all()

    session.close()

    station_names = []
    for id, name in results_stations:
        name_dict = {}
        name_dict["id"] = id
        name_dict["name"] = name
        station_names.append(name_dict)

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
#  query for the dates and temperature observations from a year from the last data point.
#  Return a JSON list of Temperature Observations (tobs) for the previous year.
def tobs():
    session = Session(engine)
    results_tobs = session.query(
        Measurement.id, 
        Measurement.station, 
        Measurement.date, 
        Measurement.tobs)\
    .filter(Measurement.date.between('2016-08-23', '2017-08-23'))\
    .order_by(Measurement.date.asc()).all()

    session.close()

    tobs_last_year = []
    for ids, station, date, tobs in results_tobs:
        tobs_dict = {}
        tobs_dict["id"] = ids
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_last_year.append(tobs_dict)
    
    return jsonify(tobs_last_year)

@app.route("/api/v1.0/start")
#  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def start():
    session = Session(engine)
    results_temp_start = session.query(
        func.distinct(Measurement.station),
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.round(func.avg(Measurement.tobs),2)
    ).filter(Measurement.date == '2016-08-23').group_by(Measurement.station).all()

    session.close()
    
    temps_start = []
    for station, tmin, tmax, tavg in results_temp_start:
        temps_start_dict = {}
        temps_start_dict["station"] = station
        temps_start_dict["temp_min"] = tmin
        temps_start_dict["temp_max"] = tmax
        temps_start_dict["temp_avg"] = tavg
        temps_start.append(temps_start_dict)

    return jsonify(temps_start)

@app.route("/api/v1.0/start/end")
#  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def end():
    session = Session(engine)
    results_temp_end = session.query(
        func.distinct(Measurement.station),
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.round(func.avg(Measurement.tobs),2)
    ).filter(Measurement.date == '2017-08-23').group_by(Measurement.station).all()

    session.close()
    
    temps_end = []
    for station, tmin, tmax, tavg in results_temp_end:
        temps_end_dict = {}
        temps_end_dict["station"] = station
        temps_end_dict["temp_min"] = tmin
        temps_end_dict["temp_max"] = tmax
        temps_end_dict["temp_avg"] = tavg
        temps_end.append(temps_end_dict)

    return jsonify(temps_end)

if __name__=="__main__":
    app.run(debug=True)