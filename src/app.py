from flask import Flask, request, abort

from dateutil import parser
import json
import pytz
import datetime
from src import static
from src.BahnScrapper import BahnScrapper

app = Flask(__name__)


@app.route('/stations', methods=['GET'])
def stations(event=None, context=None):
    return json.dumps({"stations": [str(i) for i in static.stations.keys()]})


@app.route('/search', methods=['POST'])
def search(event=None, context=None):
    data = request.get_json()
    validate(data)

    origin, destination = static.stations[data["origin"]], static.stations[data["destination"]]
    time = get_time(data)

    data = BahnScrapper().get_conn_details(origin, destination, time)

    return json.dumps(data)


def validate(data):
    if data is None or data["origin"] is None or data["destination"] is None:
        abort(404)
    if data["origin"] == data["destination"]:
        abort(404)


def get_time(data):
    if "time" not in data.keys():
        return datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))
    try:
        return parser.parse(data["time"])
    except:
        abort(418)  # I’m a teapot


if __name__ == '__main__':
    app.run()
    app.debug = True
