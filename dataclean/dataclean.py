import pandas as pd
import logging as log
import re
import json
#from LocationManager import LocationManager

log.basicConfig(filename='./dataclean.log', encoding='utf-8',format='%(asctime)s %(message)s', level=log.INFO)
log.info("Start Data Clean")

def cleanData(row):
    row['area'] = row['area'].apply(cleanArea)
    row['bathrooms'] = row['bathrooms'].apply(cleanBathroom)
    row['building_type'] = row['building_type'].apply(cleanBuildingType)
    row['department_location'] = row.apply(cleanDepartmentLocation, axis=1)
    row['rooms'] = row['rooms'].apply(cleanRooms)
    row['price'] = row['price'].apply(cleanPrice)
    return row

def removeUnusedAndNullRows(df):
    return df.drop(['date','deal_type','foreign_id','image_urls','images','location','department','title','url'],axis=1).dropna()



def cleanBathroom(bathrooms):
    # validar que mas de 3 ba;os sea 4
    if(bathrooms == 'Más de 3 baños'):
        int_baths = 4
    else:
        try:
            int_baths = int(bathrooms[0])
        except:
            int_baths = None
            log.info(f'Clean Bathroom failed to obtain number and pass it to in in string: %s',bathrooms)
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
        log.info(f'Clean Area failed to obtain number and pass it to in in string: %s',area)
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
        return dep_loc.index(this_deploc)
    else:
        log.info(f'Clean Department Location failed to validate: %s and %s',row['department'],row['location'])


def cleanPrice(price):
    try:
        price = price.replace('.','')
        pattern = r'\d+'  # Match the first set of numbers followed by optional whitespace
        price = re.findall(pattern, price)
        int_price = int(''.join(price))
    except:
        int_price = None
        log.info(f'Clean Area failed to obtain number and pass it to in in string: %s',price)
    return int_price

#print(cleanPrice('U$S 205.000'))
#print(cleanPrice('U$S 205.000'))

def cleanRooms(rooms):
    try:
        int_rooms = int(rooms)
    except:
        int_rooms = None
        log.info(f'Cannot pass rooms to int: %s',rooms)
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


#The class is created to translate between the options file and an array necesary to
# validate department and location fields
class LocationManager:
    def __init__(self):
        self.location_options_dict = None
        self.department = None
        self.departmentlocation = None
        
        self.loadDepartmentLocation()

    # Open file 
    def loadLocations(self, path='options.json'):
        with open(path) as json_file:
            location_options = json.load(json_file)
        self.location_options_dict = location_options
    
    def getDepsLocsFromObject(self):
        deps = []
        loc = []
        depsloc = []
        for department in self.location_options_dict:
            deps.append(department)
            for loc in self.location_options_dict[department]:
                deploc = department + loc
                deploc = deploc.lower().replace(' ','')
                depsloc.append(deploc)
        self.department = deps
        self.departmentlocation = depsloc

    def saveDepartmentLocation(self, path='deploc.json'):
        self.loadLocations()
        self.getDepsLocsFromObject()
        out = {'dep':self.department,
                'deploc': self.departmentlocation}
        with open(path, 'w') as file:
            json.dump(out, file)

    def loadDepartmentLocation(self, path='deploc.json'):
        with open(path) as json_file:
            deploc = json.load(json_file)
            self.departmentlocation = deploc

    def getDepartmentLocation(self):
        return self.departmentlocation['deploc']