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
class DecidimProposalPayload:

    def __init__(self):
        self.id = ''
        self.voteCount = 0
        self.title = ''

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id        

    def setVoteCount(self, voteCount):
        self.voteCount = voteCount

    def getVoteCount(self):
        return self.voteCount

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId())  +','  +\
                  '"title": ' + json.dumps(self.getTitle())  +','  +\
                  '"voteCount": ' + json.dumps(self.getVoteCount())  +\
               '}'