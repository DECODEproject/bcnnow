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

#import sys
#sys.path.append('C:/Users/mirko/Desktop/Code Repository/decode-bcnnow/')

from apps.backend.data.collectors.pull.AsiaCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.AsiaCollector.AsiaEventPayload import AsiaEventPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.TimeHelper import TimeHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
import xmltodict

# This class defines the structure of ASIA collector which adopts the pull strategy.
class AsiaEventCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + str(rID)
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data)
            total += len(data['response']['body']['resultat']['actes']['acte'])
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get ASIA data
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

    # This method builds an ASIA BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = AsiaEventPayload()
        location = LocationRecord()

        payload.setId(GeneralHelper().default(item['id']))
        payload.setName(GeneralHelper().default(item['nom']))
        payload.setEventType(GeneralHelper().toAsiaType(item['tipus_acte']))
        payload.setStartDate(TimeHelper().toDash(item['data']['data_inici']))
        payload.setEndDate(TimeHelper().toDash(item['data']['data_fi']))
        payload.setEquipmentID(GeneralHelper().default(item['lloc_simple']['id'] if 'id' in item['lloc_simple'] else ''))
        payload.setState(GeneralHelper().toAsiaState(item['estat']))
        payload.setStateCycle(GeneralHelper().toAsiaStateCycle(item['estat_cicle']))
        payload.setCategories(GeneralHelper().toClassifications(item['classificacions']))

        longitude, latitude = LocationHelper().toWGS84(GeneralHelper().default(item['lloc_simple']['adreca_simple']['coordenades']['geocodificacio']['@y']), GeneralHelper().default(item['lloc_simple']['adreca_simple']['coordenades']['geocodificacio']['@x']))
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(item['lloc_simple']['adreca_simple']['carrer']['#text'] if '#text' in item['lloc_simple']['adreca_simple']['carrer'] else ''))
        location.setStreetNumber(GeneralHelper().default(item['lloc_simple']['adreca_simple']['numero']['@enter'] if '@enter' in item['lloc_simple']['adreca_simple']['numero'] else ''))

        record.setId(GeneralHelper().default(item['id']))
        record.setSource(collectorCfg['collectors']['odi']['asia']['source_name'])
        record.setProvider('odi')
        record.setPublisher('')
        record.setType('event')
        record.setTimestamp(TimeHelper().toDash(item['data']['data_inici']))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method permanently stores an ASIA BaseRecord
    def saveData(self, data):
        items = data['response']['body']['resultat']['actes']['acte']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item).toJSON())


if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['asia']['petition_base_url']
    resourceIDs = collectorCfg['collectors']['odi']['asia']['petition_urls']
    AsiaEventCollector().start(base, resourceIDs)