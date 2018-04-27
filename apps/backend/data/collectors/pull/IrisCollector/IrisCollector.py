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

from apps.backend.data.collectors.pull.IrisCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.IrisCollector.IrisPayload import IrisPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.TimeHelper import TimeHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests

# This class defines the structure of IRIS collector which adopts the pull strategy.
class IrisCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + collectorCfg['collectors']['odi']['iris']['api_base_url'] + str(rID) + '&offset=' + str(0)
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

    # This method sends a request to get IRIS data
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

    # This method builds an IRIS BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = IrisPayload()
        location = LocationRecord()

        payload.setId(GeneralHelper().default(item['FITXA_ID']))
        payload.setArea(GeneralHelper().default(item['AREA']))
        payload.setChannel(GeneralHelper().default(item['CANALS_RESPOSTA']))
        payload.setDetail(GeneralHelper().default(item['DETALL']))
        payload.setElement(GeneralHelper().default(item['ELEMENT']))
        payload.setStartDate(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_ALTA']),
                                                 GeneralHelper().default(item['MES_DATA_ALTA']),
                                                 GeneralHelper().default(item['DIA_DATA_ALTA'])))
        payload.setEndDate(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_TANCAMENT']),
                                               GeneralHelper().default(item['MES_DATA_TANCAMENT']),
                                               GeneralHelper().default(item['DIA_DATA_TANCAMENT'])))
        payload.setSupport(GeneralHelper().default(item['SUPORT']))

        if item['LATITUD'] != None:
            location.setPoint(item['LATITUD'], item['LONGITUD'])
        else:
            location.setPoint(0.0, 0.0)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        location.setDistrict(GeneralHelper().default(item['DISTRICTE']))
        location.setNeighbourhood(GeneralHelper().default(item['BARRI']))
        location.setStreetName(
            GeneralHelper().default(item['TIPUS_VIA']) + ' ' + GeneralHelper().default(item['CARRER']))
        location.setStreetNumber(GeneralHelper().default(item['NUMERO']))

        record.setId(GeneralHelper().default(item['FITXA_ID']))
        record.setSource(collectorCfg['collectors']['odi']['iris']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(GeneralHelper().default(item['TIPUS']))
        record.setTimestamp(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_ALTA']),
                                                GeneralHelper().default(item['MES_DATA_ALTA']),
                                                GeneralHelper().default(item['DIA_DATA_ALTA'])))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an IRIS BaseRecord
    def saveData(self, data):
        items = data['result']['records']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['iris']['base_url']
    resourceIDs = collectorCfg['collectors']['odi']['iris']['complaint_urls']
    IrisCollector().start(base, resourceIDs)

