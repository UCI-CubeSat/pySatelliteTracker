import os
from datetime import datetime
import filepath
from src.python import satnogs
from pymemcache.client import base
import ast

FOLDER_PATH = filepath.getRoot() + "/CubeSAT"
FILE_DIR = FOLDER_PATH + "/tle.txt"

client = base.Client(('localhost', 11211))


def getTLE() -> {dict}:
    return satnogs.getTLE()


# def saveTLE() -> {dict}:
def saveTLE():
    data = getTLE()
    currTime = datetime.now()
    client.set("currTime", currTime)
    for key in data.keys():
        nospace_key = key.replace(" ", "_")
        line = data[key]  # line = TLE info
        client.set(nospace_key, line)

    keySet = data.keys()
    client.set("keySet", keySet)

    return data


def loadTLE() -> {dict}:
    timeStamp = client.get("currTime")
    if timeStamp == None:
        data = saveTLE()
    dateTimeObj = datetime.strptime(timeStamp.decode("utf-8"), '%Y-%m-%d %H:%M:%S.%f')
    newCurrTime = datetime.now()
    if (newCurrTime - dateTimeObj).days >= 1:
        print("WARNING: file outdated")
        saveTLE()

    data = dict()
    keySet = list(eval(client.get("keySet").decode("utf-8")))
    print(keySet)

    for k in keySet:
        nosk = k.replace(" ", "_")
        v = client.get(nosk).decode("utf-8")  # byte -> str
        data[k] = ast.literal_eval(v)  # str -> dict
    return data

# saveTLE()
# loadTLE()
