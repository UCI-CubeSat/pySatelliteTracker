import flask
import requests
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
    data = satnogs.getTLE()["ISS (ZARYA)"]
    print(data.keys())
    return flask.jsonify(calculation.getPath(data, "ISS (ZARYA)"))


if __name__ == '__main__':
    print("logging: Running on http://127.0.0.1:5000/response")
    print("logging: Running on http://127.0.0.1:5000/tle")
    print("logging: Running on http://127.0.0.1:5000/location")
    print("logging: Running on http://127.0.0.1:5000/flight_path")
    app.run(debug=True)
