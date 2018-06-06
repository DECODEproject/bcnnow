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

from apps.backend.data.collectors.pull.TouristicHouse.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.TouristicHouse.TouristicHousePayload import TouristicHousePayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.TimeHelper import TimeHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests

# This class defines the structure of HabitatgesUsTuristic collector which adopts the pull strategy.
class TouristicHouseCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + collectorCfg['collectors']['odi']['touristic_house']['api_base_url'] + str(rID) + '&offset=' + str(0)
            flag = True
            total = 0
            while flag:
                print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
                data = self.sendRequest(url)
                self.saveData(data)
                url = base + data['result']['_links']['next']
                flag = len(data['result']['records']) > 0
                total += len(data['result']['records'])
                print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get HabitatgesUsTuristic data
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

    # This method builds an HabitatgesUsTuristic BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = TouristicHousePayload()
        location = LocationRecord()

        payload.setExpedient(GeneralHelper().default(item['N_EXPEDIENT']))

        if item['LATITUD_Y'] != None:
            location.setPoint(item['LATITUD_Y'], item['LONGITUD_X'])
        else:
            location.setPoint(0.0, 0.0)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        location.setDistrict(GeneralHelper().default(item['DISTRICTE']))
        location.setNeighbourhood(GeneralHelper().default(item['BARRI']))
        location.setStreetName(GeneralHelper().default(item['TIPUS_CARRER']) + ' ' + GeneralHelper().default(item['CARRER']))
        location.setStreetNumber(GeneralHelper().default(item['TIPUS_NUM']))

        record.setId(GeneralHelper().default(item['N_EXPEDIENT']))
        record.setSource(collectorCfg['collectors']['odi']['touristic_house']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(GeneralHelper().default(item['PIS']))

        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an HabitatgesUsTuristic BaseRecord
    def saveData(self, data):
        items = data['result']['records']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['touristic_house']['base_url']
    resourceIDs = collectorCfg['collectors']['odi']['touristic_house']['habitages_urls']
    TouristicHouseCollector().start(base, resourceIDs)

