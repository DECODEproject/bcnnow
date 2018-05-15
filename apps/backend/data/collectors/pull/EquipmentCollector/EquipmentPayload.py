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

# This class defines the structure of the payload field for an instance of an ODI Equipment BaseRecord.
class EquipmentPayload:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.telephone = ''
        self.email = ''
        self.url = ''
        self.type = ''

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setTelephone(self, telephone):
        self.telephone = telephone

    def setEmail(self, email):
        self.email = email

    def setType(self, type):
        self.type = type

    def setUrl(self, url):
        self.url = url

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getTelephone(self):
        return self.telephone

    def getEmail(self):
        return self.email

    def getType(self):
        return self.type

    def getUrl(self):
        return self.url

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"type": ' + json.dumps(self.getType()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"telephone": ' + json.dumps(self.getTelephone()) +','  +\
                  '"email": ' + json.dumps(self.getEmail()) +','  +\
                  '"url": ' + json.dumps(self.getUrl()) + ''  +\
               '}'