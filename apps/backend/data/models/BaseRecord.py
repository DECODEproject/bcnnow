import json

class BaseRecord:

    def __init__(self):
        self.id = ''
        self.source = ''
        self.provider = ''
        self.publisher = ''
        self.type = ''
        self.location = {}
        self.timestamp = ''
        self.payload = {}

    def setId(self, id):
        self.id = id

    def setSource(self, source):
        self.source = source.lower()

    def setProvider(self, provider):
        self.provider = provider.lower()

    def setPublisher(self, publisher):
        self.publisher = publisher.lower()

    def setType(self, type):
        self.type = type.lower()

    def setLocation(self, location):
        self.location = location

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setPayload(self, payload):
        self.payload = payload

    def getSource(self):
        return self.source

    def getProvider(self):
        return self.provider

    def getPublisher(self):
        return self.publisher

    def getType(self):
        return self.type

    def getLocation(self):
        return self.location

    def getPayload(self):
        return self.payload

    def getTimestamp(self):
        return self.timestamp

    def getId(self):
        return self.id

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"source": ' + json.dumps(self.getSource()) +','  +\
                  '"provider": ' + json.dumps(self.getProvider()) +','  +\
                  '"publisher": ' + json.dumps(self.getPublisher()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"timestamp": ' + json.dumps(self.getTimestamp()) +','  +\
                  '"location": ' + self.getLocation().toJSON() +','  +\
                  '"payload": ' + self.getPayload().toJSON() +''  +\
               '}'