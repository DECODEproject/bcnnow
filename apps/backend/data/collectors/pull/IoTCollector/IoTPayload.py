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

# This class defines the structure of the payload field for an instance of a IoT.
class IoTPayload:

    def __init__(self):
        self.id = ''
        self.type = ''
        self.name = ''
        self.description = ''
        self.unit = ''
        self.value = 0
        self.recordedAt = ''
        self.exposure = ''

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setUnit(self, unit):
        self.unit = unit

    def getUnit(self):
        return self.unit

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setRecordedAt(self, recordedAt):
        self.recordedAt = recordedAt

    def getRecordedAt(self):
        return self.recordedAt

    def setExposure(self, exposure):
        self.exposure = exposure

    def getExposure(self):
        return self.exposure        

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId())  +','  +\
                  '"type": ' + json.dumps(self.getType())  +','  +\
                  '"name": ' + json.dumps(self.getName())  +','  +\
                  '"description": ' + json.dumps(self.getDescription())  +','  +\
                  '"unit": ' + json.dumps(self.getUnit())  +','  +\
                  '"value": ' + json.dumps(self.getValue())  +','  +\
                  '"recordedAt": ' + json.dumps(self.getRecordedAt())  +','  +\
                  '"exposure": ' + json.dumps(self.getExposure())  +''  +\
               '}'
