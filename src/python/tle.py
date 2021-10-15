import os
from datetime import datetime
import filepath
from src.python import satnogs
# THIS IS A COMMENT TO TEST GITHUB

FOLDER_PATH = filepath.getRoot() + "/CubeSAT"
FILE_DIR = FOLDER_PATH + "/tle.txt"


def getTLE() -> {dict}:
    return satnogs.getTLE()


def saveTLE() -> {dict}:
    data = getTLE()
    currTime = datetime.now()
    try:
        f = open(FILE_DIR, 'w')
    except FileNotFoundError:
        os.mkdir(FOLDER_PATH)
        f = open(FILE_DIR, 'w')
    f.write(str(currTime) + "\n")
    for key in data.keys():
        line = data[key]
        for value in line.values():
            f.write(str(value) + "\n")
    f.close()

    return data


def loadTLE() -> {dict}:
    try:
        f = open(FILE_DIR, 'r')
    except FileNotFoundError:
        print("WARNING: file not found")
        data = saveTLE()
        return data
    else:
        lines = f.readlines()
        timeStamp = lines[0].strip()
        dateTimeObj = datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S.%f')
        currTime = datetime.now()
        f.close()

        if (currTime - dateTimeObj).days >= 1:
            print("WARNING: file outdated")
            data = saveTLE()
            return data
        else:
            print("LOGGING: read existing tle file")
            keySet = ['tle0', 'tle1', 'tle2', 'tle_source', 'sat_id', 'norad_cat_id', 'updated']
            data = dict()
            for line in range(1, len(lines), len(keySet)):
                tle = dict()
                name = lines[line].strip()
                for index in range(0, len(keySet)):
                    content = lines[line + index].strip()
                    if index == 4:
                        tle[keySet[index]] = "https://db.satnogs.org/satellite/" + content
                    else:
                        tle[keySet[index]] = content
                data[name] = tle
            return data
    return dict()
