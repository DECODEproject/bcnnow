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

from apps.backend.data.collectors.pull.IoTCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.IoTCollector.IoTPayload import IoTPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

from datetime import datetime, timedelta
import requests
import json
import random
import os

import base64
from google.protobuf.timestamp_pb2 import Timestamp
from datastore_client.datastore_pb2_twirp import DatastoreClient
from datastore_client.datastore_pb2 import WriteRequest, ReadRequest
from zenroom import zenroom

# This class defines the structure of IoT collector which adopts the pull strategy.
class IoTCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, community_id, community_seckey, minutes):
        print(str(datetime.now()) + ' ' + 'Start collection')
        print(str(datetime.now()) + ' ' + '    Collecting collection for ' + community_id)
        print(str(datetime.now()) + ' ' + '        ' + ' Access to URL: ' + base)
        client = DatastoreClient(base)
        # create a read request for the policy/community of interest. Note we leave
        # `end_time` nil so we are trying to read everything up until "now"
        rr = ReadRequest()
        # the community id should be passed in by some sort of configuration rather
        # than being fixed
        rr.community_id = community_id
        # set start time to some point in the past (here we use 1 hour ago but could be
        # whatever interval the collector requires)
        start_time = datetime.utcnow() - timedelta(minutes=minutes)
        rr.start_time.FromDatetime(start_time)
        # make the first request
        resp = client.read_data(rr)
        # load the decryption script
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'decrypt.lua')) as file:
            script = file.read()
        # create decryption keys - this should be replaced with the private key loaded
        # from the environment or other configuration
        keys = '{ "community_seckey": "'+community_seckey+'" }'
        # decrypt attempts to decrypt a chunk of data using zenroom, printing out the
        # decryted values
        # now iterate through all pages of data available for the time interval
        total = 0
        while True:
            for ev in resp.events:
                # execute returns a tuple now - not sure what we should do with the err value
                result, err = zenroom.execute(script.encode(), keys=keys.encode(), data=ev.data, verbosity=1)
                # we decode the returned data and parse the json
                try:
                    msg = json.loads(result.decode("utf-8"))
                    # our actual data packet is passed as another JSON object passed as a field in the main message
                    data = json.loads(msg['data'])
                    total += self.saveData(data, community_id)
                except:
                    pass
            # if no more results then break the loop
            if resp.next_page_cursor == '':
                break
            # else get the next cursor value and fetch again
            rr.page_cursor = resp.next_page_cursor
            resp = client.read_data(rr)
        print(str(datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.now()) + ' ' + 'End collection')

    # This method builds an HabitatgesUsTuristic BaseRecord
    def buildRecord(self, item, community_id):
        record = BaseRecord()
        payload = IoTPayload()
        location = LocationRecord()
        item['recordedAt'] = (datetime.strptime(item['recordedAt'], '%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')

        latitude, longitude = GeneralHelper().default(item['latitude']), GeneralHelper().default(item['longitude'])
        location.setPoint(latitude, longitude)
        location.setAltitude(0.0)
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))

        payload.setId(GeneralHelper().default(item['token']))
        payload.setType(GeneralHelper().default(item['type']))
        payload.setName(GeneralHelper().default(item['name']))
        payload.setDescription(GeneralHelper().default(item['description']))
        payload.setUnit(GeneralHelper().default(item['unit']))
        if 'value' in item:
            payload.setValue(GeneralHelper().default(item['value']))
        elif 'values' in item:
            value = 0
            values = item['values']
            bins = item['bins']
            for i in range(len(bins)):
                value += bins[i] * values[i+1]
            payload.setValue(GeneralHelper().default(value))
        payload.setRecordedAt(GeneralHelper().default(item['recordedAt']))
        payload.setExposure(GeneralHelper().default(item['exposure']))

        record.setId(GeneralHelper().default(item['token']+'.'+item['recordedAt']))
        record.setSource(('iot__'+community_id+'__'+item['name'].lower().split()[0]).replace('-','_').replace('.','_'))
        record.setProvider('Smart Citizen')
        record.setPublisher('bcnnow')
        record.setType('event')
        record.setTimestamp(item['recordedAt'])
        record.setLocation(location)
        record.setPayload(payload)

        return record


    # This method saves a IoT BaseRecord
    def saveData(self, data, community_id):
        total = 0
        #print (data)
        item = data.copy()
        del item['sensors']
        for sensor in data['sensors']:
            StorageHelper().store(self.buildRecord({**item, **sensor},community_id).toJSON())
            total +=1 
        return total

if __name__ == "__main__":

    collectors = collectorCfg['collectors']['iot']
    for collector in collectors:
        base_url = collectorCfg['collectors']['iot'][collector]['base_url']
        community_id = collectorCfg['collectors']['iot'][collector]['community_id']
        community_seckey = collectorCfg['collectors']['iot'][collector]['community_seckey']
        minutes = collectorCfg['collectors']['iot'][collector]['minutes']
        IoTCollector().start(base_url, community_id, community_seckey, minutes)
