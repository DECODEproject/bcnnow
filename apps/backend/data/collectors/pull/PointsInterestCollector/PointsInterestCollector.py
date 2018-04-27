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

from apps.backend.data.collectors.pull.PointsInterestCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.PointsInterestCollector.PointsInterestPayload import PointsInterestPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import requests
import datetime
import xmltodict

# This class defines the structure of Points of Interest collector which adopts the pull strategy.
class PointsInterestCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + str(rID)
            total = 0
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data)
            total += len(data['opendata']['list_items']['row'])
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get Points of Interest data
    def sendRequest(self, url):
        flag = True
        while flag:
            try:
                flag = False
                response = requests.get(url=url)
                data = xmltodict.parse(response.text)
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # This method build a Points of Interest BaseRecord
    def buildRecord(self, item, type=''):
        record = BaseRecord()
        payload = PointsInterestPayload()
        location = LocationRecord()

        payload.setId(item['id'][0]['#text'])
        payload.setName(item['name']['#text'])
        payload.setType(item['type']['#text'])
        payload.setUrl(item['code_url']['#text'] if 'code_url' in item else '')
        payload.setShortDescription(item['excerpt']['#text'])
        payload.setLongDescription(item['content']['#text'])
        payload.setAssociations(GeneralHelper().toAssociations(item['code2']['item']))

        item['addresses']['item'] = item['addresses']['item'] if not isinstance(item['addresses']['item'], list) else item['addresses']['item'][0]
        longitude, latitude = item['addresses']['item']['gmapy'], item['addresses']['item']['gmapx']
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(item['addresses']['item']['address'].replace(' ' + (item['addresses']['item']['streetnum'] if 'streetnum' in item['addresses']['item'] else ''), ''))
        location.setStreetNumber(item['addresses']['item']['streetnum'] if 'streetnum' in item['addresses']['item'] else '')

        record.setId(item['id'][0]['#text'])
        record.setSource(collectorCfg['collectors']['odi']['pointsinterest']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['odi']['pointsinterest']['source_name'])
        record.setTimestamp(str(datetime.datetime.now()))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method build a Points of Interest BaseRecord
    def saveData(self, data, type=''):
        items = data['opendata']['list_items']['row']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['pointsinterest']['base_url']
    resourceIDs = collectorCfg['collectors']['odi']['pointsinterest']['poi_urls']
    PointsInterestCollector().start(base, resourceIDs)

