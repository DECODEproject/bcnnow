import json

class LocationRecord:

    def __init__(self):
        self.point = {}
        self.altitude = ''
        self.district = ''
        self.neighbourhood = ''
        self.streetName = ''
        self.streetNumber = ''
        self.city = ''

    def setPoint(self, latitude, longitude):
        self.point = {'type' : 'Point', 'coordinates' : [float(longitude) if longitude != '' and longitude != None else 0.0, float(latitude) if latitude != '' and latitude != None  else 0.0] }

    def setAltitude(self, altitude):
        self.altitude = str(altitude)

    def setDistrict(self, district):
        self.district = district

    def setNeighbourhood(self, neighbourhood):
        self.neighbourhood = neighbourhood

    def setStreetName(self, streetName):
        self.streetName = streetName

    def setStreetNumber(self, streetNumber):
        self.streetNumber = str(streetNumber)

    def setCity(self, city):
        self.city = city.title()

    def getPoint(self):
        return self.point

    def getAltitude(self):
        return self.altitude

    def getDistrict(self):
        return self.district.title()

    def getNeighbourhood(self):
        return self.neighbourhood.title()

    def getStreetName(self):
        return self.streetName.title()

    def getStreetNumber(self):
        return self.streetNumber

    def getCity(self):
        return self.city

    def toJSON(self):
        return '{'    +\
                  '"point": ' + json.dumps(self.getPoint()) +','  +\
                  '"altitude": ' + json.dumps(self.getAltitude()) +','  +\
                  '"district": ' + json.dumps(self.getDistrict()) +','  +\
                  '"neighbourhood": ' + json.dumps(self.getNeighbourhood()) +','  +\
                  '"city": ' + json.dumps(self.getCity()) +','  +\
                  '"streetname": ' + json.dumps(self.getStreetName()) +','  +\
                  '"streetnumber": ' + json.dumps(self.getStreetNumber()) + '' +\
               '}'