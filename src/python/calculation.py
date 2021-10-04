import time
import numpy
from skyfield.toposlib import wgs84
from skyfield.api import EarthSatellite, load
from datetime import datetime


def selectSat(tle: dict, name: str) -> dict:
    if name not in tle.keys():
        return dict()

    return dict(tle0=tle.values()["tle0"], tle1=tle.values()["tle1"], tle2=tle.values()["tle2"])


def getFlightPath(data: dict, duration: float = 10 * 3600, resolution: float = 4.0) -> dict:
    response = dict()
    satellite = EarthSatellite(data["tle1"], data["tle2"], data["tle0"], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second

    interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute,
                      numpy.arange(start, start + duration, resolution * 60))
    location = satellite.at(interval)
    path = wgs84.subpoint(location)

    response["identifier"] = data["tle0"]
    response["origin"] = (wgs84.subpoint(satellite.at(t)).latitude.degrees,
                          wgs84.subpoint(satellite.at(t)).longitude.degrees)
    response["latArray"] = path.latitude.degrees
    response["longArray"] = path.longitude.degrees