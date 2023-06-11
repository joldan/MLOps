import pandas as pd
import logging as log
from sys import path
import re
import json
import os
import numpy as np
from os.path import dirname, abspath
from LocationManager import LocationManager

rootPath = dirname(dirname(abspath(__file__)))
# Import myLog
logPath= rootPath+"/log/"
path.append(logPath)
from myLog import *

log.info(f"Main -> %s - DataClean Loading",__name__)


#from LocationManager import LocationManager

def cleanData(row):
    row['area'] = row['area'].apply(cleanArea)
    row['bathrooms'] = row['bathrooms'].apply(cleanBathroom)
    row['building_type'] = row['building_type'].apply(cleanBuildingType)
    row['department_location'] = row.apply(cleanDepartmentLocation, axis=1)
    row['rooms'] = row['rooms'].apply(cleanRooms)
    row['price'] = row['price'].apply(cleanPrice)
    log.info(f"Main -> %s - Function %s invoked, data cleaned",__name__,cleanData.__name__)
    return row

def removeUnusedAndNullRows(df):
    df2 = df.fillna(np.nan)
    df2 = df.dropna()
    return df2[['id', 'area','rooms','bathrooms','building_type','department_location', 'price']]

def saveCleanData(df, path='cleanData.csv'):
    df.to_csv(path, index=False)

def removeUnusedPhotos(df):
    dropped_rows = df[df.isnull().any(axis=1)]
    dropped_rows_id = dropped_rows['id']
    remove_files_from_path(dropped_rows_id)

def remove_files_from_path(filenames, path):
    for filename in filenames:
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            log.info(f"Main -> %s - File '{filename}' removed successfully.",__name__)
        else:
            log.info(f"Main -> %s - File '{filename}' does not exist.",__name__)


def cleanBathroom(bathrooms):
    # validar que mas de 3 ba;os sea 4
    if(bathrooms == 'Más de 3 baños'):
        int_baths = 4
    else:
        try:
            int_baths = int(bathrooms[0])
        except:
            int_baths = None
            log.info(f'Main -> %s - Clean Bathroom failed to obtain number and pass it to in in string: %s',__name__,bathrooms)
    return int_baths

#print(cleanBathroom('Más de 3 baños'))
#print(cleanBathroom('1 Baños'))

def cleanArea(area):
    try:
        pattern = r'^\d+\s*'  # Match the first set of numbers followed by optional whitespace
        area_number = re.match(pattern, area)[0]
        int_area = int(area_number)
        if(int_area < 25):
            int_area = 25
        elif(int_area > 500):
            int_area = 500
    except:
        int_area = None
        log.info(f'Main -> %s - Clean Area failed to obtain number and pass it to in in string: %s',__name__,area)
    return int_area

#print(cleanArea('16 Mts'))
#print(cleanArea('50 Mts'))
#print(cleanArea('100 Mts'))
#print(cleanArea('600 Mts'))

def cleanDepartmentLocation(row):
    loc = LocationManager()
    dep_loc = loc.getDepartmentLocation()
    this_deploc = row['department'] + row['location']
    this_deploc = this_deploc.lower().replace(' ','')
    if(this_deploc in dep_loc):
        data =  dep_loc.index(this_deploc)
        log.info(f'Main -> %s - Function %s invoke - DepLoc index:%s',__name__,cleanDepartmentLocation.__name__,data)
        return data
    else:
        log.info(f'Main -> %s - Function %s invoke - Clean Department Location failed to validate: %s and %s',__name__,cleanDepartmentLocation.__name__,row['department'],row['location'])
        return None

def cleanPrice(price):
    try:
        price = price.replace('.','')
        pattern = r'\d+'  # Match the first set of numbers followed by optional whitespace
        price = re.findall(pattern, price)
        int_price = int(''.join(price))
    except:
        int_price = None
        log.info(f'Main -> %s - Clean Area failed to obtain number and pass it to in in string: %s',__name__,price)
    return int_price

#print(cleanPrice('U$S 205.000'))
#print(cleanPrice('U$S 205.000'))

def cleanRooms(rooms):
    try:
        int_rooms = int(rooms)
    except:
        int_rooms = None
        log.info(f'Main -> %s - Cannot pass rooms to int: %s',__name__,rooms)
    return int_rooms

def cleanBuildingType(building_type):
    binary_building_type = 0
    if(building_type == 'Casa'):
        binary_building_type = 1
    elif(building_type == "Apartamento"):
        binary_building_type = 0
    else:
        binary_building_type = None
    return binary_building_type

