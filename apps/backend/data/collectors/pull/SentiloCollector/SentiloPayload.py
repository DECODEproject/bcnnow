import json

class SentiloPayload:

    def __init__(self):
        self.value = 0
        self.emplacament = ''
        self.type = ''
        self.unit = ''
        self.description = ''

    def setValue(self, value):
        self.value = value

    def setEmplacament(self, emplacament):
        self.emplacament = emplacament

    def setType(self, type):
        self.type = type

    def setUnit(self, unit):
        self.unit = unit

    def setDescription(self, description):
        self.description = description

    def getEmplacament(self):
        return self.emplacament

    def getType(self):
        return self.type

    def getUnit(self):
        return self.unit

    def getDescription(self):
        return self.description

    def getValue(self):
        return self.value

    def toJSON(self):
        return '{'    +\
                  '"value": ' + json.dumps(self.getValue()) + ',' +\
                  '"emplacament": ' + json.dumps(self.getEmplacament()) + ',' +\
                  '"description": ' + json.dumps(self.getDescription()) + ',' +\
                  '"unit": ' + json.dumps(self.getUnit()) + ',' +\
                  '"type": ' + json.dumps(self.getType()) + '' +\
               '}'