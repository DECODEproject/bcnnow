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

# This class defines the structure of the payload field for an instance of an IRIS BaseRecord.
class TouristicHousePayload:

    def __init__(self):
        self.habitatgesUsTuristicID = ''
        self.nExpedient = ''

    def setId(self, habitatgesUsTuristicID):
        self.habitatgesUsTuristicID = habitatgesUsTuristicID

    def setExpedient(self, nExpedient):
        self.nExpedient = nExpedient.title()

    def getId(self):
        return self.habitatgesUsTuristicID

    def getExpedient(self):
        return self.nExpedient

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"nExpedient": ' + json.dumps(self.getExpedient())  +\
               '}'