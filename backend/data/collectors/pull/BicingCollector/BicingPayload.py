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

# This class defines the structure of the payload field for an instance of a Bicing BaseRecord.
class BicingPayload:

    def __init__(self):
        self.id = ''
        self.type = ''
        self.nearbyStationIDs = ''
        self.slots = 0
        self.bikes = 0
        self.status = ''

    def setId(self, id):
        self.id = id

    def setType(self, type):
        self.type = type.lower()

    def setNearbyStationIDs(self, nearbyStationIDs):
        self.nearbyStationIDs = nearbyStationIDs

    def setSlots(self, slots):
        self.slots = float(slots)

    def setBikes(self, bikes):
        self.bikes = float(bikes)

    def setStatus(self, status):
        self.status = status.lower()

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getNearbyStationIDs(self):
        return self.nearbyStationIDs

    def getSlots(self):
        return self.slots

    def getBikes(self):
        return self.bikes

    def getStatus(self):
        return self.status

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"status": ' + json.dumps(self.getStatus()) +','  +\
                  '"neabystationids": ' + json.dumps(self.getNearbyStationIDs()) +','  +\
                  '"slots": ' + json.dumps(self.getSlots()) +','  +\
                  '"bikes": ' + json.dumps(self.getBikes()) + '' +\
               '}'