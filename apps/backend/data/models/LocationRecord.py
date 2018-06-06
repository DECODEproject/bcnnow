'''
    BarcelonaNow (c) Copyright 2018 by the Eurecat - Technology Centre of Catalonia

    This source code is free software; you can redistribute it and/or
    modify it under the terms of the GNU Public License as published
    by the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This source code is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Please refer to the GNU Public License for more details.

    You should have received a copy of the GNU Public License along with
    this source code; if not, write to:
    Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''

import json

# This class defines the basic structure of the location field contained into an instance of a BaseRecord.
class LocationRecord:

    def __init__(self):
        self.point = {}
        self.altitude = ''
        self.district = ''
        self.neighbourhood = ''
        self.streetName = ''
        self.streetNumber = ''
        self.city = ''
        self.geometry = {}

    def setPoint(self, latitude, longitude):
        self.point = {'type' : 'Point', 'coordinates' : [float(longitude) if longitude != '' and longitude != None else 0.0, float(latitude) if latitude != '' and latitude != None  else 0.0] }

    def setGeometry(self, geometry):
        self.geometry = geometry

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

    def getGeometry(self):
        return self.geometry

    def getCity(self):
        return self.city

    def toJSON(self):
        return '{'    +\
                  '"point": ' + json.dumps(self.getPoint()) +','  +\
                  '"geometry": ' + json.dumps(self.getGeometry()) +','  +\
                  '"altitude": ' + json.dumps(self.getAltitude()) +','  +\
                  '"district": ' + json.dumps(self.getDistrict()) +','  +\
                  '"neighbourhood": ' + json.dumps(self.getNeighbourhood()) +','  +\
                  '"city": ' + json.dumps(self.getCity()) +','  +\
                  '"streetname": ' + json.dumps(self.getStreetName()) +','  +\
                  '"streetnumber": ' + json.dumps(self.getStreetNumber()) + '' +\
               '}'