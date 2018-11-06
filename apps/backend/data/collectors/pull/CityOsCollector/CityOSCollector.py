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



import pymongo
from pymongo import MongoClient
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

#from apps.backend.data.collectors.pull.CityOsCollector.Config import Config as collectorConfig

#collectorCfg = collectorConfig().get()

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
    def start(self):

        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        print('Get Config Details from mongodb')
        try:
            client = MongoClient(globalCfg['storage']['ipaddress'], globalCfg['storage']['port'])
            db = client[globalCfg['storage']['dbname']]
            collection = db[globalCfg["collectors"]["common"]["collection"]]
            query = {"source_name":"cityos"}
            result=collection.find(query)
            if(result.count()==0):
                print("no config found!!")
                sys.exit(-1)
            else:
                print('Done reading config')
                collectorCfg=result[0]
                max_features = 1000
                resourceIDs=collectorCfg['config']['datasets']
                base=collectorCfg['config']['base_url']
                for rindex, rID in enumerate(resourceIDs):
                    print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
                    rurl = base + '&typeName=' + str(rID) + '&maxFeatures=' + str(max_features)
                    flag = True
                    total = 90048
                    while flag:
                        url = rurl + '&startIndex=' + str(total)
                        print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
                        data = self.sendRequest(url,collectorCfg)
                        self.saveData(data, rID)
                        flag = len(data['features']) == max_features
                        total += len(data['features'])
                    print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                    print(str(datetime.datetime.now()) + ' ' + 'End collection')

        except:
            print
            "Unexpected error:", sys.exc_info()[0]
            raise



    # This method sends a request to get CityOS data
    def sendRequest(self, url,collectorCfg):
        flag = True
        request_count=0
        while flag:
            try:
                flag = False
                token_response = requests.post(collectorCfg['config']['token_url'],
                                         data=collectorCfg['config']['data'],
                                         verify=False,
                                         allow_redirects=False,
                                         auth=(collectorCfg['config']['credentials']['client_id'],
                                               collectorCfg['config']['credentials']['client_secret']))

                if(token_response.status_code==200):
                    token = json.loads(token_response.text)['access_token']
                    headers = collectorCfg['config']['headers']
                    headers['Authorization'] = 'Bearer ' + token
                    data_response = requests.get(url, headers=headers, verify=False)
                    data = data_response.json()
                    return data
                else:
                    print(token_response.text)
                    sys.exit(-1)


            except:
                print
                "Unable to connect:", sys.exc_info()[0]
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                request_count+=1
                if(request_count==10):
                    raise
                else:
                    flag=True

    # This method builds a CityOS BaseRecord
    def buildRecord(self, item, type):

        if type == "cityos:potencial_fotovoltaic":
            LocationHelper().toWGS84Geometry(item['geometry'], 'EPSG:25831', isNested=True)
            payload = CityOSPVPotentialPayload()
            payload.setId(item['id'])
            payload.setPowTh(item['properties']['POW_TH'])
            payload.setEventCode(item['properties']['EventCode'])
            payload.setSuitability(item['properties']['SUITABILITY'])
            payload.setSumModare(item['properties']['SUM_MODARE'])
            payload.setPolygon(item['geometry'])
        elif type == "cityos:ptt_carril_bici":
            LocationHelper().toWGS84Geometry(item['geometry'], 'EPSG:25831')
            payload = CityOSBikeLinesPayload()
            payload.setId(item['id'])
            payload.setId1(item['properties']['ID1'])
            payload.setId2(item['properties']['ID2'])
            payload.setEventCode(item['properties']['EventCode'])
            payload.setLine(item['geometry'])

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
        print(data)
        items = data['features']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, type).toJSON())

if __name__ == "__main__":
    CityOSCollector().start()
