# -*- coding: utf-8 -*-

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

from apps.backend.data.collectors.pull.DecidimCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.DecidimCollector.DecidimProposalPayload import DecidimProposalPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
from shapely.geometry import shape

# This class defines the structure of HabitatgesUsTuristic collector which adopts the pull strategy.
class DecidimProposalCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[], source_name=None):
        component_id = collectorCfg['collectors']['decidim'][source_name]['component_id']
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)

            url = base
            flag = True
            total = 0
            endCursor = ''
            while flag:
                print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url  + '        ' + ' endCursor: ' + endCursor )
                data = self.sendRequest(url, rID.replace('""','"'+endCursor+'"'))
                total += self.saveData(data, component_id)
                endCursor = data['data']['participatoryProcess']['components'][component_id]['proposals']['pageInfo']['endCursor']
                flag = endCursor != None
                print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get HabitatgesUsTuristic data
    def sendRequest(self, url, query):
        flag = True
        while flag:
            try:
                flag = False
                response = requests.post(url, data = {'query': query})
                data = response.json()
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + 'Reconnecting...')
                flag = True

    # This method builds an HabitatgesUsTuristic BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = DecidimProposalPayload()
        location = LocationRecord()

        payload.setId(GeneralHelper().default(item['id']))
        payload.setTitle(GeneralHelper().default(item['title']))
        payload.setVoteCount(GeneralHelper().default(item['voteCount']))
        payload.setTotalCommentsCount(GeneralHelper().default(item['totalCommentsCount']))
        if 'category' in item: payload.setCategory(GeneralHelper().default(item['category']['name']['translations'][0]['text']))

        if 'scope' in item:
            coords = shape(LocationHelper().getAreaGeometry(item['scope']['name']['translations'][0]['text'].replace(' - ','-'), 'neighbourhood_group')).centroid
            location.setDistrict(GeneralHelper().default(item['scope']['name']['translations'][0]['text'].replace(' - ','-').strip()))
            payload.setDistrict(GeneralHelper().default(item['scope']['name']['translations'][0]['text'].replace(' - ','-').strip()))
            location.setNeighbourhood(GeneralHelper().default(''))
            longitude, latitude = coords.x, coords.y
            location.setPoint(latitude, longitude)
            location.setAltitude(0.0)
            location.setCity('Barcelona')
            location.setStreetName(GeneralHelper().default(''))
            location.setStreetNumber(GeneralHelper().default(''))

        record.setId(GeneralHelper().default(item['reference']))
        record.setSource(source_name)
        record.setProvider('decidim')
        record.setPublisher('bcnnow')
        record.setType(source_name)
        record.setTimestamp(item['publishedAt'])
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves a DecidimProposal BaseRecord
    def saveData(self, data, component_id=0):
        total = 0
        items = data['data']['participatoryProcess']['components'][component_id]['proposals']['edges']
        if len(items) >= 0:
            for index, item in enumerate(items):
                if item['node'] != None:
                    StorageHelper().store(self.buildRecord(item['node']).toJSON())
                    total += 1
        return total

if __name__ == "__main__":
    source_name = 'dddc_proposal'
    base = collectorCfg['collectors']['decidim'][source_name]['base_url']
    resourceIDs = collectorCfg['collectors']['decidim'][source_name]['query']
    DecidimProposalCollector().start(base, resourceIDs, source_name)
    
    source_name = 'pam_proposal'
    base = collectorCfg['collectors']['decidim'][source_name]['base_url']
    resourceIDs = collectorCfg['collectors']['decidim'][source_name]['query']
    DecidimProposalCollector().start(base, resourceIDs, source_name)
