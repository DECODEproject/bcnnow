import json

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