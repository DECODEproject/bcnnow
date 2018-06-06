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

# This class defines the structure of the payload field for an instance of a CityOS BaseRecord.
class CityOSBikeLinesPayload:

    def __init__(self):
        self.id = ''
        self.id1 = ''
        self.id2 = ''
        self.line = []
        self.eventCode = 0

    def setId(self, id):
        self.id = str(id)

    def setId1(self, id1):
        self.id1 = str(id1)

    def setId2(self, id2):
        self.id2 = str(id2)

    def setLine(self, line):
        self.line = line

    def setEventCode(self, eventCode):
        self.eventCode = float(eventCode)

    def getId(self):
        return self.id

    def getId1(self):
        return self.id1

    def getId2(self):
        return self.id2

    def getLine(self):
        return self.line

    def getEventCode(self):
        return self.eventCode

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"id1": ' + json.dumps(self.getId1()) +','  +\
                  '"id2": ' + json.dumps(self.getId2()) +','  +\
                  '"line": ' + json.dumps(self.getLine()) +','  +\
                  '"eventCode": ' + json.dumps(self.getEventCode()) +\
               '}'