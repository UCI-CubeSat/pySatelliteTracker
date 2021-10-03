import flask
from src.python import tle

app = flask.Flask(__name__)

payload = {"key": "value"}


@app.route('/payload', methods=['GET'])
def getPayload():
    return flask.jsonify(tle.loadTLE())


if __name__ == '__main__':
    print("logging: Running on http://127.0.0.1:5000/payload")
    app.run(debug=True)
