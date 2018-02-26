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

# This class defines the structure of the payload field for an instance of a Sentilo BaseRecord.
class SentiloPayload:

    def __init__(self):
        self.value = ''
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