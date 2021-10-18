import subprocess
from sys import platform as _platform
from datetime import datetime
from src.python import satnogs, filepath
from pymemcache.client import base
import ast

FOLDER_PATH = filepath.getRoot() + "/CubeSAT"
FILE_DIR = FOLDER_PATH + "/tle.txt"

client = base.Client(('localhost', 11211))


def getTLE() -> {dict}:
    return satnogs.getTLE()


def saveTLE() -> {dict}:
    if _platform == "win32":
        return getTLE()

    data = getTLE()
    currTime = datetime.now()
    client.set("currTime", currTime)
    client.set("keySet", data.keys())
    for key in data.keys():
        cacheKey = key.replace(" ", "_")
        line = data[key]  # line = TLE info
        client.set(cacheKey, line)

    return data


def loadTLE() -> {dict}:
    if _platform == "win32":
        print("WARNING: cache miss")
        return getTLE()

    try:
        timeStamp = client.get("currTime")
    except ConnectionRefusedError:
        timeStamp = None
        subprocess.run(["brew", "services", "start", "memcached"])

    if timeStamp is None:
        print("WARNING: cache miss")
        data = saveTLE()
        return data

    dateTimeObj = datetime.strptime(timeStamp.decode("utf-8"), '%Y-%m-%d %H:%M:%S.%f')
    newCurrTime = datetime.now()
    if (newCurrTime - dateTimeObj).days >= 1:
        print("WARNING: cache outdated")
        data = saveTLE()
        return data

    print("LOGGING: cache hit")
    data = dict()
    keySetString = client.get("keySet").decode("utf-8")
    keySet = ast.literal_eval(keySetString[10:-1])

    for k in keySet:
        key = k.replace(" ", "_")
        v = client.get(key).decode("utf-8")  # byte -> str
        data[k] = ast.literal_eval(v)  # str -> dict
    return data
