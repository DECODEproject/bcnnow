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

# This class defines the basic structure of the records to be stored.
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