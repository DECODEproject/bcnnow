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

from backend.data.collectors.pull.EquipmentCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from backend.data.collectors.pull.EquipmentCollector.EquipmentPayload import AsiaEquipmentPayload
from backend.data.models.BaseRecord import BaseRecord
from backend.data.models.LocationRecord import LocationRecord
from backend.data.helpers.LocationHelper import LocationHelper
from backend.data.helpers.GeneralHelper import GeneralHelper
from backend.data.helpers.StorageHelper import StorageHelper

import requests
import datetime
import xmltodict

# This class defines the structure of ODI Equipment collector which adopts the pull strategy.
class EquipmentCollector:

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
            self.saveData(data, type=rID.replace('.rdf', ''))
            total += len(data['rdf:RDF']['v:VCard'])
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get ODI Equipment data
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

    # This method build an ODI Equipment BaseRecord
    def buildRecord(self, item, type=''):
        record = BaseRecord()
        payload = AsiaEquipmentPayload()
        location = LocationRecord()

        payload.setId(item['dct:identifier'])
        payload.setType(type)
        payload.setEmail((item['v:email']['rdf:Description']['@rdf:about'] if not isinstance(item['v:email'], list) else item['v:email'][0]['rdf:Description']['@rdf:about']) if 'v:email' in item else '')
        payload.setUrl((item['v:url']['@rdf:resource'] if not isinstance(item['v:url'], list) else item['v:url'][0]['@rdf:resource']) if 'v:url' in item else '')
        payload.setName(item['v:fn'])
        payload.setTelephone((item['v:tel']['rdf:Description']['rdf:value'] if not isinstance(item['v:tel'], list) else item['v:tel'][0]['rdf:Description']['rdf:value']) if 'v:tel' in item else '')
        longitude, latitude = (item['v:geo']['v:Location']['v:longitude'] if not isinstance(item['v:geo'], list) else item['v:geo'][0]['v:Location']['v:longitude']), (item['v:geo']['v:Location']['v:latitude'] if not isinstance(item['v:geo'], list) else item['v:geo'][0]['v:Location']['v:latitude'])
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))

        if 'v:adr' in item:
            location.setStreetName(((item['v:adr']['v:Address']['xv:streetAddress']['xv:Street']['xv:streetName'] if 'xv:streetName' in item['v:adr']['v:Address']['xv:streetAddress']['xv:Street'] else '') if 'xv:streetAddress' in item['v:adr']['v:Address'] else '') if not isinstance(item['v:adr'], list) else ((item['v:adr'][0]['v:Address']['xv:streetAddress']['xv:Street']['xv:streetName'] if 'xv:streetName' in item['v:adr'][0]['v:Address']['xv:streetAddress']['xv:Street']['xv:streetName'] else '') if 'xv:streetAddress' in item['v:adr'][0]['v:Address'] else ''))
            location.setStreetNumber(((item['v:adr']['v:Address']['xv:streetAddress']['xv:Street']['xv:streetNumber'] if 'xv:streetNumber' in item['v:adr']['v:Address']['xv:streetAddress']['xv:Street'] else '') if 'xv:streetAddress' in item['v:adr']['v:Address'] else '') if not isinstance(item['v:adr'], list) else ((item['v:adr'][0]['v:Address']['xv:streetAddress']['xv:Street']['xv:streetNumber'] if 'xv:streetNumber' in item['v:adr'][0]['v:Address']['xv:streetAddress']['xv:Street'] else '') if 'xv:streetAddress' in item['v:adr'][0]['v:Address'] else ''))

        record.setId(item['dct:identifier'])
        record.setSource(collectorCfg['collectors']['odi']['equipment']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['odi']['equipment']['source_name'])
        record.setTimestamp(str(datetime.datetime.now()))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an ODI Equipment BaseRecord
    def saveData(self, data, type=''):
        items = data['rdf:RDF']['v:VCard']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, type).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['asia']['equipment_base_url']
    resourceIDs = collectorCfg['collectors']['odi']['asia']['equipment_urls']
    EquipmentCollector().start(base, resourceIDs)

