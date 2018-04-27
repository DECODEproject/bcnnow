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
import sys
sys.path.append('Insert your path to the BarcelonaNow project folder')

from apps.backend.data.collectors.pull.InsideAirbnbCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.InsideAirbnbCollector.InsideAirbnbCalendarPayload import InsideAirbnbCalendarPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.StorageHelper import StorageHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper

import pandas as pd
import datetime

# This class defines the structure of Inside Airbnb Calendar collector which adopts the pull strategy.
class InsideAirbnbCalendarCollector:

    def __init__(self, ):
        return

    # This methods starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + str(rID)
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data)
            total += len(data.index)
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get Inside Airbnb Calendar data
    def sendRequest(self, url):
        return pd.read_csv(url)

    # This method build an Inside Airbnb Calendar BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = InsideAirbnbCalendarPayload()
        location = LocationRecord()

        payload.setListingId(item['listing_id'])
        payload.setAvailable(item['available'])
        payload.setPrice(item['price'])

        longitude, latitude = GeneralHelper().default(''), GeneralHelper().default('')
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(''))
        location.setStreetNumber(GeneralHelper().default(''))

        record.setId(str(item['listing_id']) + '.' + item['date'].replace(' ', ''))
        record.setSource(collectorCfg['collectors']['insideairbnb']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['insideairbnb']['calendar_source_name'])
        record.setTimestamp(item['date'])
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an Inside Airbnb Calendar BaseRecord
    def saveData(self, data):
        items = data
        if len(items.index) >= 0:
            for index, item in items.iterrows():
                StorageHelper().store(self.buildRecord(item).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['insideairbnb']['base_url']
    resourceIDs = collectorCfg['collectors']['insideairbnb']['calendar_urls']
    InsideAirbnbCalendarCollector().start(base, resourceIDs)