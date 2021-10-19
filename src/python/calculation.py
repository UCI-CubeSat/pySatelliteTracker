import collections

import numpy
from skyfield.toposlib import wgs84
from skyfield.api import EarthSatellite, load
from skyfield.timelib import Time
import src.python.tle as tle


def selectSat(tle: dict, name: str) -> dict:
    if name not in tle.keys():
        return dict()

    return tle[name]


def getPath(data: dict, mode: str = "latlong", duration: float = 10 * 3600, resolution: float = 4.0) -> dict:
    if mode == "latlong":
        return getSphericalPath(data, duration, resolution)
    if mode == "xyz":
        return getCartesianPath(data, duration, resolution)
    return getSphericalPath(data, duration, resolution)


def getSphericalPath(data: dict, duration: float, resolution: float) -> dict:
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
    response["elevationArray"] = path.elevation.au
    response["interval"] = interval

    return response


def getCartesianPath(data, duration, resolution):
    response = dict()
    satellite = EarthSatellite(data["tle1"], data["tle2"], data["tle0"], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second

    interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute,
                      numpy.arange(start, start + duration, resolution * 60))
    location = satellite.at(interval)
    d = numpy.array([])

    for i in range(len(location.position.km[0])):
        numpy.append(d, (numpy.linalg.norm(numpy.array(
            [location.position.km[0][i], location.position.km[1][i], location.position.km[2][i]])
                                           - numpy.array([0, 0, 0]))))

    response["identifier"] = data["tle0"]
    response["x"] = location.position.km[0]
    response["y"] = location.position.km[1]
    response["z"] = location.position.km[2]
    response["d"] = d  # euclidean distance
    response["interval"] = interval

    return response


def getSerializedPath(data: dict):
    for k in data.keys():
        if str(type(data[k])) == "<class 'numpy.ndarray'>":
            data[k] = data[k].tolist()

    return data


def getSerializedHorizon(data: list):
    for index in range(0, len(data)):
        data[index] = str(data[index])

    return data


def findHorizonTime(data, duration, receiverLocation: wgs84.latlon) -> list:
    satellite = EarthSatellite(data["tle1"], data["tle2"], data["tle0"], load.timescale())
    ts = load.timescale()
    start = load.timescale().now()
    if_temp = start.utc
    t_utc = start.utc

    end = ts.utc(t_utc.year, t_utc.month, t_utc.day, t_utc.hour, t_utc.minute, t_utc.second + duration)
    condition = {"bare": 0, "marginal": 25.0, "good": 50.0, "excellent": 75.0}
    degree = condition["bare"]  # peak is at 90
    t_utc, events = satellite.find_events(receiverLocation, start, end, altitude_degrees=degree)


    # events = [2,0,1,2,0,1]
    print("before loop events: ", events)
    if list(events[:3]) != [0,1,2]:
        print("inside check first if")
        start = ts.utc(if_temp.year, if_temp.month, if_temp.day, if_temp.hour, if_temp.minute, if_temp.second - 15*60)
        t_utc, events = satellite.find_events(receiverLocation, start, end, altitude_degrees=degree)
    if list(events[-3:]) != [0,1,2]:
        print("inside check second if")
        end = ts.utc(if_temp.year, if_temp.month, if_temp.day, if_temp.hour, if_temp.minute, if_temp.second + duration + 7*48*3600)
        t_utc, events = satellite.find_events(receiverLocation, start, end, altitude_degrees=degree)
        print("after loop events: ", events)

    # FOR DEBUG
    # SEE HOW IT NORMALLY ALWAYS HAVE [riseabove, culminate, setbelow]
    print(start.utc_strftime('%Y %b %d %H:%M:%S'), "-", end.utc_strftime('%Y %b %d %H:%M:%S'))
    for ti, event in zip(t_utc, events):
        name = (f'rise above {degree}°', 'culminate', f'set below {degree}°')[event]
        print(f'{ti.utc_strftime("%Y %b %d %H:%M:%S")} {name}', end="")
        if "set below" in name:
            print("")
        else:
            print(", ", end="")
    # END DEBUG

    intervals = []
    for index in range(0, len(events), 3):
        try:
            t_utc[index + 2]
        except IndexError:
            # break

            # our quick fix here is just to break out of for loop
            # when len(t_utc) != 3
            # but instead we should look back/forward in time and find
            # either the missing datetime_rise or datetime_peak

            # print(f'ERROR: for Satellite - {data["tle0"]}, for Duration - {duration/3600.0} hrs')
            # print("During: ", start.utc_strftime('%Y %b %d %H:%M:%S'), "-", end.utc_strftime('%Y %b %d %H:%M:%S'))
            # for ti, event in zip(t_utc, events):
            #     name = (f'rise above {degree}°', 'culminate', f'set below {degree}°')[event]
            #     print(f'{ti.utc_strftime("%Y %b %d %H:%M:%S")} {name}', end="")
            #     if "rise above" in name:
            #         print(", ", end="")
            #     elif "set below" in name:
            #         print("")
            #     else:
            #         print(", ", end="")
            #
            # print("\nMissing either a rise above or set below")
            raise IndexError
        else:
            datetime_rise = Time.utc_datetime(t_utc[index])
            datetime_peak = Time.utc_datetime(t_utc[index + 1])
            datetime_set = Time.utc_datetime(t_utc[index + 2])
            t0 = ts.utc(datetime_rise.year, datetime_rise.month, datetime_rise.day, datetime_rise.hour,
                        datetime_rise.minute, datetime_rise.second)

            diff = numpy.float64((datetime_set - datetime_rise).total_seconds())
            t0_sec = t0.utc.second
            t1_sec = t0_sec + diff
            intervals.append(
                (ts.utc(t0.utc.year, t0.utc.month, t0.utc.day, t0.utc.hour, t0.utc.minute,
                        numpy.arange(t0_sec, t1_sec, 60)),
                 datetime_peak))

    return intervals


# if __name__ == "__main__":
    # findHorizonTime(tle.loadTLE()["ISS (ZARYA)"], 5*24*3600, wgs84.latlon(33.643831, -117.841132, elevation_m=17))