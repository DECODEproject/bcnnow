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

# This class defines the structure of the payload field for an instance of a Decidim Proposal.
class DecidimMeetingPayload:

    def __init__(self):
        self.id = ''
        self.attendeeCount = 0
        self.title = ''
        self.startTime = ''
        self.endTime = ''
        self.address = ''
        self.attachments = []            

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id        

    def setAttendeeCount(self, attendeeCount):
        self.attendeeCount = attendeeCount

    def getAttendeeCount(self):
        return self.attendeeCount

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def setStartTime(self, startTime):
        self.startTime = startTime

    def getStartTime(self):
        return self.startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getEndTime(self):
        return self.endTime

    def setAddress(self, address):
        self.address = address

    def getAddress(self):
        return self.address

    def setAttachments(self, attachments):
        self.attachments = attachments

    def getAttachments(self):
        return self.attachments

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId())  +','  +\
                  '"attendeeCount": ' + json.dumps(self.getAttendeeCount()) + ',' +\
                  '"title": ' + json.dumps(self.getTitle())  +','  +\
                  '"startTime": ' + json.dumps(self.getStartTime())  +','  +\
                  '"endTime": ' + json.dumps(self.getEndTime())  +','  +\
                  '"address": ' + json.dumps(self.getAddress())  +','  +\
                  '"attachments": ' + json.dumps(self.getAttachments())  +''  +\
               '}'
