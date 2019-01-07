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

from apps.backend.data.collectors.pull.DecidimCollector.DecidimMeetingPayload import DecidimMeetingPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
import json
import random

# This class defines the structure of HabitatgesUsTuristic collector which adopts the pull strategy.
class DecidimMeetingCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
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
                total += self.saveData(data)
                endCursor = data['data']['participatoryProcess']['components'][1]['meetings']['pageInfo']['endCursor']
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
        payload = DecidimMeetingPayload()
        location = LocationRecord()

        latitude, longitude = GeneralHelper().default(item['coordinates']['latitude']), GeneralHelper().default(item['coordinates']['longitude'])
        location.setPoint(latitude, longitude)
        location.setAltitude(0.0)
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(item['address'].split(',')[0]))
        location.setStreetNumber(GeneralHelper().default(int(item['address'].split(',')[1]) if len(item['address'].split(',')[1].strip()) in [1,2] else '') if len(item['address'].split(','))>1 else '')

        payload.setId(GeneralHelper().default(item['reference']))
        payload.setAttendeeCount(GeneralHelper().default(item['attendeeCount']))
        payload.setTitle(GeneralHelper().default(item['title']['translations'][0]['text']))
        payload.setStartTime(GeneralHelper().default(item['startTime']))
        payload.setEndTime(GeneralHelper().default(item['endTime']))
        payload.setAddress(GeneralHelper().default(item['address']))
        attachments = []
        for attachment in item['attachments']:
            attachments.append(attachment['url'])
        payload.setAttachments(GeneralHelper().default(attachments))

        record.setId(GeneralHelper().default(item['reference']))
        record.setSource(collectorCfg['collectors']['decidim']['pam_meeting']['source_name'])
        record.setProvider('decidim')
        record.setPublisher('bcnnow')
        record.setType(collectorCfg['collectors']['decidim']['pam_meeting']['source_name'])
        record.setTimestamp(item['startTime'])
        record.setLocation(location)
        record.setPayload(payload)

        return record


    # This method saves a DecidimMeeting BaseRecord
    def saveData(self, data):
        total = 0
        items = data['data']['participatoryProcess']['components'][1]['meetings']['edges']
        if len(items) >= 0:
            for index, item in enumerate(items):
                if item['node'] != None:
                    StorageHelper().store(self.buildRecord(item['node']).toJSON())
                    total += 1
        return total

if __name__ == "__main__":
    base = collectorCfg['collectors']['decidim']['pam_meeting']['base_url']
    resourceIDs = collectorCfg['collectors']['decidim']['pam_meeting']['query']
    DecidimMeetingCollector().start(base, resourceIDs)

