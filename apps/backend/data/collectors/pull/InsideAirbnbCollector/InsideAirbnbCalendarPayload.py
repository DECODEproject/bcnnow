import json

class InsideAirbnbCalendarPayload:

    def __init__(self):
        self.listingId = ''
        self.available = ''
        self.price = 0

    def setListingId(self, listingId):
        self.listingId = str(listingId)

    def setAvailable(self, available):
        self.available = str(available)

    def setPrice(self, price):
        self.price = float(price)

    def getListingId(self):
        return self.listingId

    def getAvailable(self):
        return self.available

    def getPrice(self):
        return self.price

    def toJSON(self):
        return '{'    +\
                  '"listingid": ' + json.dumps(self.getListingId()) +','  +\
                  '"available": ' + json.dumps(self.getAvailable()) +','  +\
                  '"price": ' + json.dumps(self.getPrice()) + '' +\
               '}'
