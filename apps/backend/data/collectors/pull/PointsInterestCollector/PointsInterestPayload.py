import json

class PointsInterestPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.type = ''
        self.url = ''
        self.shortDescription = ''
        self.longDescription = ''
        self.notes = ''
        self.associations = {}

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setUrl(self, url):
        self.url = url

    def setShortDescription(self, shortDescription):
        self.shortDescription = shortDescription

    def setLongDescription(self, longDescription):
        self.longDescription = longDescription

    def setNotes(self, notes):
        self.notes = notes

    def setAssociations(self, associations):
        self.associations = associations

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getUrl(self):
        return self.url

    def getShortDescription(self):
        return self.shortDescription

    def getLongDescription(self):
        return self.longDescription

    def getNotes(self):
        return self.notes

    def getAssociations(self):
        return self.associations

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"url": ' + json.dumps(self.getUrl()) +','  +\
                  '"shortdescription": ' + json.dumps(self.getShortDescription()) +','  +\
                  '"longdescription": ' + json.dumps(self.getLongDescription()) +',' +\
                  '"notes": ' + json.dumps(self.getNotes()) +','  +\
                  '"associations": ' + json.dumps(self.getAssociations()) +'' +\
               '}'