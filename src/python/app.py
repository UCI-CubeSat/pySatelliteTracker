import flask
import requests

from src.python import tle, geocoding, satnogs

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


if __name__ == '__main__':
    print("logging: Running on http://127.0.0.1:5000/response")
    print("logging: Running on http://127.0.0.1:5000/tle")
    print("logging: Running on http://127.0.0.1:5000/location")
    app.run(debug=True)
