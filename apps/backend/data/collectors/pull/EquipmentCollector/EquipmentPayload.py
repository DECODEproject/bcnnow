import json

class AsiaEquipmentPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.telephone = ''
        self.email = ''
        self.url = ''
        self.type = ''

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setTelephone(self, telephone):
        self.telephone = telephone

    def setEmail(self, email):
        self.email = email

    def setType(self, type):
        self.type = type

    def setUrl(self, url):
        self.url = url

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getTelephone(self):
        return self.telephone

    def getEmail(self):
        return self.email

    def getType(self):
        return self.type

    def getUrl(self):
        return self.url

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"telephone": ' + json.dumps(self.getTelephone()) +','  +\
                  '"email": ' + json.dumps(self.getEmail()) +','  +\
                  '"url": ' + json.dumps(self.getUrl()) + ''  +\
               '}'