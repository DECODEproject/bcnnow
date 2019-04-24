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

import sys, os

from apps.backend.data.collectors.pull.DecidimCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.DecidimCollector.DecidimPetitionCredentialPayload import DecidimPetitionCredentialPayload
from apps.backend.data.collectors.pull.DecidimCollector.DecidimPetitionSignaturePayload import DecidimPetitionSignaturePayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper
from zenroom import zenroom
from hashlib import sha256

import datetime
import requests
import json
import random
import subprocess
from shapely.geometry import shape

# This class defines the structure of DecidimPetition collector which adopts the pull strategy.
class DecidimPetitionCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, source_name=None, districts=None):

        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        dddc_api_url = base['dddc_api_url']
        query = base['query']
        response = requests.post(dddc_api_url, data = {'query': query}, headers={'accept': 'application/json'})

        petition = response.json()['data']['petition']
        print (petition)
        petition_id = petition['attribute_id']
        credential_issuer_api_url = petition['credential_issuer_api_url']

        json_attribute_info_optional = petition['json_attribute_info_optional']
        hashed_bins = {}
        for attribute in json_attribute_info_optional:
            value_set = attribute['value_set']
            for value in value_set:
                result, _ = zenroom.execute(script="print(ECDH.kdf(HASH.new('sha512'), str(DATA)))".encode(), keys=None, data=value.encode())
                hashed_bins[result.decode()] = value

        credentials_url = base['credentials_url']
        response = requests.get(credentials_url+'/stats/', headers={'accept': 'application/json'})
        stats = response.json()
        item_count = 0
        total = stats['total']
        del stats['total']
        for attribute in stats:
            attribute_stats = stats[attribute]
            attribute_total_count = 0
            for attribute_stat in attribute_stats:
                attribute_value = list(attribute_stat.keys())[0]
                attribute_count = attribute_stat[attribute_value]
                if attribute_value in hashed_bins:
                    attribute_total_count += attribute_count
                    for i in range(attribute_count):
                        item = {}
                        item['id'] = petition_id + '-' + str(item_count)
                        item['petitionId'] = petition_id
                        item['age'] = None
                        item['gender'] = None
                        item['district'] = None
                        if 'district' == attribute:
                            item[attribute] = districts[str(hashed_bins[attribute_value])]
                        else:
                            item[attribute] = hashed_bins[attribute_value]
                        print (item)
                        StorageHelper().store(self.buildCredentialRecord(item).toJSON())
                        item_count += 1
            # fill with not provided data
            #for i in range(total-attribute_total_count):
            #    item = {}
            #    item['id'] = petition_id + '-' + str(item_count)
            #    item['petitionId'] = petition_id
            #    item['age'] = None
            #    item['gender'] = None
            #    item['district'] = None
            #    item[attribute] = 'not provided'
            #    StorageHelper().store(self.buildCredentialRecord(item).toJSON())
            #    item_count += 1

        print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

        for petition_id in collectorCfg['collectors']['decidim'][source_name]['petitions_ids']:

            petitions_url = collectorCfg['collectors']['decidim'][source_name]['petitions_url']
            dddc_username = collectorCfg['collectors']['decidim'][source_name]['dddc_username']
            dddc_password = collectorCfg['collectors']['decidim'][source_name]['dddc_password']

            print ('----------------------')
            print ('Token:')
            response = requests.post(petitions_url+'/token', data = 'grant_type=&username='+dddc_username+'&password='+dddc_password+'&scope=&client_id=&client_secret=', headers={'accept': 'application/json' , 'content-type' : 'application/x-www-form-urlencoded'})
            access_token = response.json()['access_token']
            print (access_token)
            print ('----------------------')
            print ('Count:')
            response = requests.post(petitions_url+'/petitions/'+petition_id+'/count', headers={'authorization' : 'Bearer ' + access_token ,'accept': 'application/json' , 'content-type' : 'application/json'})
            count = response.json()
            print (count)
            print ('----------------------')
            print ('Get (Expanded):')
            response = requests.get(petitions_url+'/petitions/'+petition_id+'?expand=True', headers={'accept': 'application/json' , 'content-type' : 'application/json'})
            result = response.json()
            print (result)
            print ('----------------------')
            print ('Assert count:')
            tally = result['tally']
            petition = result['petition']
            print ('Executing contract from zenroom...')
            f = open('/tmp/tally.json', 'w')
            f.write(json.dumps(tally, indent=2))
            f.close()   
            f = open('/tmp/petition.json', 'w')
            f.write(json.dumps(petition, indent=2))
            f.close()   
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(__location__, '14-CITIZEN-count-petition.zencode')) as file:
                petition_count_zencode = file.read()
            command = 'zenroom -k /tmp/tally.json -a /tmp/petition.json -z ' + (os.path.join(__location__, '14-CITIZEN-count-petition.zencode'))
            assert_count = json.loads(subprocess.check_output(command.split()).decode("utf-8"))
            if (assert_count==count):
                print ( 'Everything was validated perfectly! Result:', str(assert_count['result']))
                for i in range(count['result']):
                    item = {}
                    item['id'] = petition_id + '-' + str(item_count)
                    item['petitionId'] = petition_id
                    StorageHelper().store(self.buildSignatureRecord(item).toJSON())
                    item_count += 1
            else:
                print ( 'Uh oh! Couldn\'t validate results')
            #result, _ = zenroom.execute(script=petition_count_zencode.encode(), keys='/tmp/tally.json', data='/tmp/petition.json')


    # This method builds an DecidimPetitionCredential BaseRecord
    def buildCredentialRecord(self, item):
        record = BaseRecord()
        payload = DecidimPetitionCredentialPayload()
        location = LocationRecord()                
        
        if not item['district'] == None and not item['district'] == 'not provided':
            coords = shape(LocationHelper().getAreaGeometry(item['district'].replace(' - ','-'), 'neighbourhood_group')).centroid
            location.setDistrict(GeneralHelper().default(item['district']))
            payload.setDistrict(GeneralHelper().default(item['district']))
            location.setNeighbourhood(GeneralHelper().default(''))
            longitude, latitude = coords.x, coords.y
            location.setPoint(latitude, longitude)
            location.setAltitude(0.0)
            location.setCity('Barcelona')
            location.setStreetName(GeneralHelper().default(''))
            location.setStreetNumber(GeneralHelper().default(''))

        payload.setId(GeneralHelper().default(item['id']))
        payload.setPetitionId(GeneralHelper().default(item['petitionId']))
        payload.setAge(GeneralHelper().default(item['age']))
        payload.setGender(GeneralHelper().default(item['gender']))
        payload.setDistrict(GeneralHelper().default(item['district']))
        payload.setStartTime(str(datetime.datetime.now()))
        payload.setEndTime(str(datetime.datetime.now()))

        record.setId(GeneralHelper().default(item['id']))
        record.setSource(source_name+'_credential')
        record.setProvider('decidim')
        record.setPublisher('bcnnow')
        record.setType(source_name)
        record.setTimestamp(str(datetime.datetime.now()))
        
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method builds an DecidimPetitionSignature BaseRecord
    def buildSignatureRecord(self, item):
        record = BaseRecord()
        payload = DecidimPetitionSignaturePayload()
        location = LocationRecord()                
        
        payload.setId(GeneralHelper().default(item['id']))
        payload.setPetitionId(GeneralHelper().default(item['petitionId']))
        payload.setLabel('signature')
        payload.setStartTime(str(datetime.datetime.now()))
        payload.setEndTime(str(datetime.datetime.now()))

        record.setId(GeneralHelper().default(item['id']))
        record.setSource(source_name+'_signature')
        record.setProvider('decidim')
        record.setPublisher('bcnnow')
        record.setType(source_name)
        record.setTimestamp(str(datetime.datetime.now()))
        
        record.setLocation(location)
        record.setPayload(payload)

        return record

if __name__ == "__main__":

    source_name = 'dddc_petition'
    base = collectorCfg['collectors']['decidim'][source_name]
    districts = collectorCfg['districts']
    DecidimPetitionCollector().start(base, source_name, districts)