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

# This class defines the structure of the payload field for an instance of an Inside Airbnb Calendar BaseRecord.
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
