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

# This class defines the structure of the payload field for an instance of a Decidim Petition Signature.
class DecidimPetitionSignaturePayload:

    def __init__(self):
        self.id = ''
        self.petitionId = ''
        self.label = ''
        self.startTime = ''
        self.endTime = ''

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id        

    def setPetitionId(self, petitionId):
        self.petitionId = petitionId

    def getPetitionId(self):
        return self.petitionId        

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getStartTime(self):
        return self.startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getEndTime(self):
        return self.endTime

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId())  +','  +\
                  '"petitionId": ' + json.dumps(self.getPetitionId())  +','  +\
                  '"label": ' + json.dumps(self.getLabel())  +','  +\
                  '"startTime": ' + json.dumps(self.getStartTime())  +','  +\
                  '"endTime": ' + json.dumps(self.getEndTime())  +\
               '}'
