import os
from datetime import datetime
import filepath
from src.python import satnogs

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
    else:
        f.write(str(currTime) + "\n")
        for key in data.keys():
            line = data[key]
            for value in line.values():
                f.write(str(value) + "\n")
        f.close()

    return data


def loadTLE() -> [dict]:
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

        if (currTime - dateTimeObj).days >= 1:
            print("WARNING: file outdated")
            data = saveTLE()
            return data
        else:
            print("LOGGING: read existing tle file")
            data = []
            for line in range(1, len(lines), 7):
                keys = ['tle0', 'tle1', 'tle2', 'tle_source', 'url', 'norad_cat_id']
                tle = dict()
                for k in range(6):
                    if k == 4:
                        tle[keys[k]] = "https://db.satnogs.org/satellite/" + lines[line + k].strip()
                    else:
                        tle[keys[k]] = lines[line + k].strip()
                data.append(tle)
            return data
    return []
