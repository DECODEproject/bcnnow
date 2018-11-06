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


from apps.backend.data.collectors.pull.OHBCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.OHBCollector.OHBPayload import OHBPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.StorageHelper import StorageHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper

from shapely.geometry import shape
import pandas as pd
import datetime

# This class defines the structure of Inside Airbnb Listing collector which adopts the pull strategy.
class OHBCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        for rindex, rID in enumerate(resourceIDs):
          #  print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + str(rID)
           # print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data, rID)
            total += len(data.index)
            #print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get OHB data
    def sendRequest(self, url):
        return pd.read_csv(url, low_memory=False)

    # This method build an OHB Listing BaseRecord
    def buildRecord(self, item, type):
        record = BaseRecord()
        payload = OHBPayload()
        location = LocationRecord()

        payload.setPeriod(item['PERIODE'])
        payload.setValue(item['ind_value'])

        if 'Districts' in type:
            coords = shape(LocationHelper().getAreaGeometry(item['NOM'], 'neighbourhood_group')).centroid
            location.setDistrict(GeneralHelper().default(item['NOM'].strip()))
            location.setNeighbourhood(GeneralHelper().default(''))
        else:
            coords = shape(LocationHelper().getAreaGeometry(item['NOM'], 'neighbourhood')).centroid
            location.setDistrict(GeneralHelper().default(''))
            location.setNeighbourhood(GeneralHelper().default(item['NOM'].strip()))

        longitude, latitude = coords.x, coords.y
        location.setPoint(latitude, longitude)
        location.setAltitude(0.0)
        location.setCity('Barcelona')
        location.setStreetName(GeneralHelper().default(''))
        location.setStreetNumber(GeneralHelper().default(''))

        record.setId(str(item['PERIODE'])[:4] + '_' + item['CODI_OHB'])
        record.setSource(collectorCfg['collectors']['OHB']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(type.replace('.csv', ''))
        record.setTimestamp(str(item['PERIODE'])[:4] + '-01-01T00:00:00Z')
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an OHB Airbnb Listin BaseRecord
    def saveData(self, data, type):
        items = data
        if len(items.index) >= 0:
            for index, item in items.iterrows():
                StorageHelper().store(self.buildRecord(item, type).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['OHB']['base_url']
    resourceIDs = collectorCfg['collectors']['OHB']['paths']
    OHBCollector().start(base, resourceIDs)