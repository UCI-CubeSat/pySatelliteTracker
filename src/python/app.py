import flask
import requests
from skyfield.toposlib import wgs84

from src.python import tle, geocoding, satnogs, calculation

app = flask.Flask(__name__)


@app.route('/response', methods=['GET'])
def getResponse():
    return flask.jsonify(requests.get(satnogs.TLE_URL).json())


@app.route('/tle', methods=['GET'])
def getPayload():
    return flask.jsonify(tle.loadTLE())


@app.route('/location', methods=['GET'])
def getLatLong():
    return flask.jsonify(geocoding.getLatLong()[1])


@app.route('/flight_path', methods=['GET'])
def getCalculation():
    data = tle.loadTLE()["ISS (ZARYA)"]
    return flask.jsonify(calculation.getSerializePath(calculation.getPath(data, "latlong")))


@app.route('/flight_horizon', methods=['GET'])
def getHorizon():
    data = tle.loadTLE()["ISS (ZARYA)"]
    return flask.jsonify(calculation.getSerializedHorizon(calculation.findHorizonTime(data, 3*24*3600,
                                                                                      wgs84.latlon(33.643831,
                                                                                                   -117.841132,
                                                                                                   elevation_m=17))))


if __name__ == '__main__':
    print("logging: Running on http://127.0.0.1:5000/response")
    print("logging: Running on http://127.0.0.1:5000/tle")
    print("logging: Running on http://127.0.0.1:5000/location")
    print("logging: Running on http://127.0.0.1:5000/flight_path")
    print("logging: Running on http://127.0.0.1:5000/flight_horizon")
    app.run(debug=True)
