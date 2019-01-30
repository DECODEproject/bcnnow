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

from apps.backend.data.collectors.pull.DecidimCollector.DecidimSurveyPayload import DecidimSurveyPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
import json
import random
import os


# This class defines the structure of HabitatgesUsTuristic collector which adopts the pull strategy.
class DecidimSurveyCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base+rID
            total = 0
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            os.chdir(os.path.dirname(__file__))
            with open(url) as f:
                data = json.load(f)
            total += self.saveData(data,rID)
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
            print(str(datetime.datetime.now()) + ' ' + 'End collection')


    # This method builds an HabitatgesUsTuristic BaseRecord
    def buildRecord(self, item, rID, index):
        record = BaseRecord()
        payload = DecidimSurveyPayload()
        location = LocationRecord()

        payload.setId(GeneralHelper().default(rID.replace('.json','-')+index))
        payload.setGender(GeneralHelper().default(item['gender']))
        payload.setAge(GeneralHelper().default(item['age']))
        payload.setCountry(GeneralHelper().default(item['country']))
        payload.setContinent(GeneralHelper().default(item['continent']))
        payload.setEducation(GeneralHelper().default(item['education']))
        if 'work situation' in item: payload.setWorkSituation(GeneralHelper().default(item['work situation']))
        payload.setOrganization(GeneralHelper().default(item['organization']))
        payload.setCity(GeneralHelper().default(item['city']))
        if 'district' in item: payload.setDistrict(GeneralHelper().default(item['district']))
        payload.setDevice(GeneralHelper().default(item['device']))
        if 'scale' in item: payload.setScale(GeneralHelper().default(item['scale']))
        payload.setInterest(GeneralHelper().default(item['interest']))
        record.setId(GeneralHelper().default(rID.replace('.json','-')+index))
        record.setSource(collectorCfg['collectors']['decidim']['dddc_survey']['source_name'])
        record.setProvider('decidim')
        record.setPublisher('bcnnow')
        record.setType(collectorCfg['collectors']['decidim']['dddc_survey']['source_name'])
        record.setTimestamp(str(datetime.datetime.now()).split('.')[0])

        record.setLocation(location)
        record.setPayload(payload)

        return record


    # This method saves a DecidimSurvey BaseRecord
    def saveData(self, data, rID):
        total = 0
        items = data
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, rID, str(index)).toJSON())
                total += 1
        return total

if __name__ == "__main__":
    base = collectorCfg['collectors']['decidim']['dddc_survey']['base_url']
    resourceIDs = collectorCfg['collectors']['decidim']['dddc_survey']['paths']
    DecidimSurveyCollector().start(base, resourceIDs)

