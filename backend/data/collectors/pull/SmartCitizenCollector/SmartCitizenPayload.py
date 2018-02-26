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

# This class defines the structure of the payload field for an instance of a Smart Citizen BaseRecord.
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