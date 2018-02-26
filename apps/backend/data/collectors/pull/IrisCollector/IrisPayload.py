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
class IrisPayload:

    def __init__(self):
        self.irisID = ''
        self.area = ''
        self.element = ''
        self.detail = ''
        self.support = ''
        self.channel = ''
        self.startDate = ''
        self.endDate = ''

    def setId(self, irisid):
        self.irisID = irisid

    def setArea(self, area):
        self.area = area.title()

    def setElement(self, element):
        self.element = element.title()

    def setDetail(self, detail):
        self.detail = detail.title()

    def setSupport(self, support):
        self.support = support.title()

    def setChannel(self, channel):
        self.channel = channel.title()

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    def getId(self):
        return self.irisID

    def getArea(self):
        return self.area

    def getElement(self):
        return self.element

    def getDetail(self):
        return self.detail

    def getSupport(self):
        return self.support

    def getChannel(self):
        return self.channel

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"area": ' + json.dumps(self.getArea()) +','  +\
                  '"element": ' + json.dumps(self.getElement()) +','  +\
                  '"detail": ' + json.dumps(self.getDetail()) +','  +\
                  '"support": ' + json.dumps(self.getSupport()) +','  +\
                  '"channel": ' + json.dumps(self.getChannel()) +','  +\
                  '"startdate": ' + json.dumps(self.getStartDate()) +',' +\
                  '"enddate": ' + json.dumps(self.getEndDate()) + ''  +\
               '}'