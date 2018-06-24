import json

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