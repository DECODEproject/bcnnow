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

from apps.backend.data.collectors.pull import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull import BicingPayload
from apps.backend.data.models import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data import LocationHelper
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper
import datetime
import requests

# This class defines the structure of Bicing collector which adopts the pull strategy.
class BicingCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        url = base
        print(str(datetime.datetime.now()) + ' ' + '    ' + ' Access to URL: ' + url)
        data = self.sendRequest(url)
        self.saveData(data)
        total += len(data['stations'])
        print(str(datetime.datetime.now()) + ' ' + '     Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get Bicing data
    def sendRequest(self, url):
        flag = True
        while flag:
            try:
                flag = False
                response = requests.get(url=url)
                data = response.json()
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # This method builds a Bicing BaseRecord
    def buildRecord(self, item, start_date):
        record = BaseRecord()
        payload = BicingPayload()
        location = LocationRecord()

        payload.setId(item['id'])
        payload.setSlots(item['slots'])
        payload.setNearbyStationIDs([station for station in item['nearbyStations'].split(' ')])
        payload.setBikes(item['bikes'])
        payload.setType(item['type'])
        payload.setStatus(item['status'])

        longitude, latitude = GeneralHelper().default(item['longitude']), GeneralHelper().default(item['latitude'])
        location.setPoint(latitude, longitude)
        location.setAltitude(GeneralHelper().default(item['altitude']))
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(item['streetName']))
        location.setStreetNumber(GeneralHelper().default(item['streetNumber']))

        record.setId(item['id'] + '.' + start_date)
        record.setSource(collectorCfg['collectors']['odi']['bicing']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['odi']['bicing']['source_name'])
        record.setTimestamp(start_date)
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method permanently stores a Bicing BaseRecord
    def saveData(self, data):
        start_date = str(datetime.datetime.now())
        items = data['stations']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, start_date).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['bicing']['base_url']
    BicingCollector().start(base)