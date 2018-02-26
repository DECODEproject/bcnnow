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

# This class defines the structure of the payload field for an instance of an Inside Airbnb Review BaseRecord.
class InsideAirbnbReviewPayload:

    def __init__(self):
        self.id = ''
        self.listingID = ''
        self.date = ''
        self.reviewerID = ''
        self.reviewerName = ''
        self.comments = ''

    def setId(self, id):
        self.id = str(id)

    def setListingID(self, listingID):
        self.listingID = str(listingID)

    def setDate(self, date):
        self.date = str(date)

    def setReviewerID(self, reviewerID):
        self.reviewerID = str(reviewerID)

    def setReviewerName(self, reviewerName):
        self.reviewerName = str(reviewerName)

    def setComments(self, comments):
        self.comments = str(comments)

    def getId(self):
        return self.id

    def getListingID(self):
        return self.listingID

    def getDate(self):
        return self.date

    def getReviewerID(self):
        return self.reviewerID

    def getReviewerName(self):
        return self.reviewerName

    def getComments(self):
        return self.comments

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"listingid": ' + json.dumps(self.getListingID()) +','  +\
                  '"date": ' + json.dumps(self.getDate()) +','  +\
                  '"reviewerid": ' + json.dumps(self.getReviewerID()) +','  +\
                  '"reviewername": ' + json.dumps(self.getReviewerName()) +','  +\
                  '"comments": ' + json.dumps(self.getComments()) + '' +\
               '}'