import json

class AsiaEventPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.equipmentID = ''
        self.startDate = ''
        self.endDate = ''
        self.eventType = ''
        self.state = ''
        self.categories = []
        self.stateCycle = ''

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setEquipmentID(self, equipmentID):
        self.equipmentID = equipmentID

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    def setEventType(self, eventType):
        self.eventType = eventType

    def setState(self, state):
        self.state = state

    def setCategories(self, categories):
        self.categories = categories

    def setStateCycle(self, stateCycle):
        self.stateCycle = stateCycle

    def getName(self):
        return self.name

    def getEquipmentID(self):
        return self.equipmentID

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def getEventType(self):
        return self.eventType

    def getState(self):
        return self.state

    def getCategories(self):
        return self.categories

    def getStateCycle(self):
        return self.stateCycle

    def getId(self):
        return self.id

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"equipmentid": ' + json.dumps(self.getEquipmentID()) +','  +\
                  '"startdate": ' + json.dumps(self.getStartDate()) +','  +\
                  '"enddate": ' + json.dumps(self.getEndDate()) +','  +\
                  '"eventtype": ' + json.dumps(self.getEventType()) +','  +\
                  '"state": ' + json.dumps(self.getState()) +','  +\
                  '"statecycle": ' + json.dumps(self.getStateCycle()) +','  +\
                  '"categories": ' + json.dumps(self.getCategories()) + '' +\
               '}'