import json

class SmartCitizenPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.description = ''
        self.state = ''
        self.addedAt = ''
        self.value = 0

    def setId(self, id):
        self.id = str(id)

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setState(self, state):
        self.state = state

    def setAddedAt(self, addedAt):
        self.addedAt = addedAt

    def setValue(self, value):
        self.value = float(value)

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getState(self):
        return self.state

    def getAddedAt(self):
        return self.addedAt

    def getValue(self):
        return self.value

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) + ','  +\
                  '"name": ' + json.dumps(self.getName()) + ','  +\
                  '"description": ' + json.dumps(self.getDescription()) + ','  +\
                  '"state": ' + json.dumps(self.getState()) + ','  +\
                  '"addedat": ' + json.dumps(self.getAddedAt()) +',' +\
                  '"value": ' + json.dumps(self.getValue()) + '' +\
               '}'