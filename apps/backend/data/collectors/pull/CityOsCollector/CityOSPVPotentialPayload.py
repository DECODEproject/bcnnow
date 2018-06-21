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
class CityOSPVPotentialPayload:

    def __init__(self):
        self.id = ''
        self.powTh = 0
        self.polygon = []
        self.eventCode = ''
        self.suitability = ''
        self.sumModare = ''

    def setId(self, id):
        self.id = str(id)

    def setPowTh(self, powTh):
        if powTh != "":
            self.powTh = float(powTh)

    def setPolygon(self, polygon):
        self.polygon = polygon

    def setEventCode(self, eventCode):
        self.eventCode = str(eventCode)

    def setSuitability(self, suitability):
        self.suitability = str(suitability)

    def setSumModare(self, sumModare):
        self.sumModare = str(sumModare)

    def getId(self):
        return self.id

    def getPowTh(self):
        return self.powTh

    def getPolygon(self):
        return self.polygon

    def getEventCode(self):
        return self.eventCode

    def getSuitability(self):
        return self.suitability

    def getSumModare(self):
        return self.sumModare

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"powth": ' + json.dumps(self.getPowTh()) +','  +\
                  '"polygon": ' + json.dumps(self.getPolygon()) +','  +\
                  '"eventCode": ' + json.dumps(self.getEventCode()) +','  +\
                  '"suitability": ' + json.dumps(self.getSuitability()) +','  +\
                  '"sumModare": ' + json.dumps(self.getSumModare()) +\
               '}'