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

# This class defines the structure of the payload field for an instance of a Points of Interest BaseRecord.
class PointsInterestPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.type = ''
        self.url = ''
        self.shortDescription = ''
        self.longDescription = ''
        self.notes = ''
        self.associations = {}

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setUrl(self, url):
        self.url = url

    def setShortDescription(self, shortDescription):
        self.shortDescription = shortDescription

    def setLongDescription(self, longDescription):
        self.longDescription = longDescription

    def setNotes(self, notes):
        self.notes = notes

    def setAssociations(self, associations):
        self.associations = associations

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getUrl(self):
        return self.url

    def getShortDescription(self):
        return self.shortDescription

    def getLongDescription(self):
        return self.longDescription

    def getNotes(self):
        return self.notes

    def getAssociations(self):
        return self.associations

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"url": ' + json.dumps(self.getUrl()) +','  +\
                  '"shortdescription": ' + json.dumps(self.getShortDescription()) +','  +\
                  '"longdescription": ' + json.dumps(self.getLongDescription()) +',' +\
                  '"notes": ' + json.dumps(self.getNotes()) +','  +\
                  '"associations": ' + json.dumps(self.getAssociations()) +'' +\
               '}'