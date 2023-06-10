#The class is created to translate between the options file and an array necesary to
# validate department and location fields
from os.path import dirname, abspath

class LocationManager:
    def __init__(self):
        self.location_options_dict = None
        self.department = None
        self.departmentlocation = None
        
        self.loadDepartmentLocation()
        rootPath = dirname(dirname(abspath(__file__)))
        rootConf = rootPath+"conf/"

    # Open file 
    def loadLocations(self, path='options.json'):
        with open(rootConf+path) as json_file:
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
        with open(rootConf+path, 'w') as file:
            json.dump(out, file)

    def loadDepartmentLocation(self, path='deploc.json'):
        with open(rootConf+path) as json_file:
            deploc = json.load(json_file)
            self.departmentlocation = deploc

    def getDepartmentLocation(self):
        return self.departmentlocation