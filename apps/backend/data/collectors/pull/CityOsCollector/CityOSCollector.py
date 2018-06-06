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
sys.path.append('/home/code/projects/decode-bcnnow/')

from apps.backend.data.collectors.pull.CityOsCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()


from apps.backend.data.collectors.pull.CityOsCollector.CityOSBikeLinesPayload import CityOSBikeLinesPayload
from apps.backend.data.collectors.pull.CityOsCollector.CityOSPVPotentialPayload import CityOSPVPotentialPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper
from shapely.geometry import shape, Point
import datetime
import requests
import json

import warnings
warnings.filterwarnings('ignore')

# This class defines the structure of CityOS collector which adopts the pull strategy.
class CityOSCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        max_features = 1000
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            rurl = base + '&typeName=' + str(rID) + '&maxFeatures=' + str(max_features)
            flag = True
            total = 0
            while flag:
                url = rurl + '&startIndex' + str(total)
                print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
                data = self.sendRequest(url)
                self.saveData(data, rID)
                flag = len(data['features']) == max_features
                total += len(data['features'])
                print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get CityOS data
    def sendRequest(self, url):
        flag = True
        while flag:
            try:
                flag = False
                token_response = requests.post(collectorCfg['collectors']['cityos']['token_url'],
                                         data=collectorCfg['tokens']['cityos']['data'],
                                         verify=False,
                                         allow_redirects=False,
                                         auth=(collectorCfg['tokens']['cityos']['credentials']['client_id'],
                                               collectorCfg['tokens']['cityos']['credentials']['client_secret']))
                token = json.loads(token_response.text)['access_token']
                headers = collectorCfg['tokens']['cityos']['headers']
                headers['Authorization'] = 'Bearer ' + token
                data_response = requests.get(url, headers=headers, verify=False)
                data = data_response.json()
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # This method builds a CityOS BaseRecord
    def buildRecord(self, item, type):
        LocationHelper().toWGS84Geometry(item['geometry'], 'EPSG:25831')

        if type == "cityos:potencial_fotovoltaic":
            payload = CityOSPVPotentialPayload()
            payload.setId(item['id'])
            payload.setPowTh(item['properties']['POW_TH'])
            payload.setEventCode(item['properties']['EventCode'])
            payload.setSuitability(item['properties']['SUITABILITY'])
            payload.setSumModare(item['properties']['SUM_MODARE'])
        elif type == "cityos:ptt_carril_bici":
            payload = CityOSBikeLinesPayload()
            payload.setId(item['id'])
            payload.setId1(item['properties']['ID1'])
            payload.setId2(item['properties']['ID2'])
            payload.setEventCode(item['properties']['EventCode'])

        location = LocationRecord()
        coords = shape(item['geometry']).centroid
        longitude, latitude = coords.x, coords.y
        location.setPoint(latitude, longitude)
        location.setAltitude(GeneralHelper().default(0))
        location.setCity('')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(''))
        location.setStreetNumber(GeneralHelper().default(''))
        location.setGeometry(item['geometry'])

        record = BaseRecord()
        record.setId(item['id'])
        record.setSource(type.split(':')[0] + '-' + type.split(':')[1])
        record.setProvider(type.split(':')[0])
        record.setPublisher('')
        record.setType(type.split(':')[1])
        record.setTimestamp(item['properties']['MD_DATA_PUBLISHED'])
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method permanently stores a CityOS BaseRecord
    def saveData(self, data, type):
        items = data['features']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, type).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['cityos']['base_url']
    CityOSCollector().start(collectorCfg['collectors']['cityos']['base_url'],
                            collectorCfg['collectors']['cityos']['datasets'])
