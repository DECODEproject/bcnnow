import sys


from apps.backend.data.collectors.pull.SmartCitizenCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.SmartCitizenCollector.SmartCitizenPayload import SmartCitizenPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
import re
import os
import pickle

class SmartCitizentCollector:

    def __init__(self, ):
        return

    # Start reader process
    def start(self, base):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        lastUrl = globalCfg['project']['base_url'] + 'backend/data/collectors/polling/SmartCitizenCollector/history/smartcitizen-last-readings.pkl'
        lastReadings = pickle.load(open(lastUrl, 'rb')) if os.path.isfile(lastUrl) else {}
        total = 0
        resourceIDs = self.getAllSensors()
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    ' + str(rindex+1) + '/' + str(len(resourceIDs)) + ' Collecting data for ' + rID['name'])
            start = lastReadings[rID['id']] if rID['id'] in lastReadings else '2017-01-01T00:00:00Z'
            a = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
            b = datetime.timedelta(days=90)
            end = (a + b).strftime("%Y-%m-%dT%H:%M:%SZ")
            while datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ') < datetime.datetime.now():
                url = base + str(rID['id']) + '/readings?sensor_id=' + str(23) + '&rollup=1h&from=' + start + '&to=' + end
                print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
                data = self.sendRequest(url)
                self.saveData(data, rID)
                a = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
                b = datetime.timedelta(seconds=1)
                start = (a + b).strftime("%Y-%m-%dT%H:%M:%SZ")
                a = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
                b = datetime.timedelta(days=90)
                end = (a + b).strftime("%Y-%m-%dT%H:%M:%SZ")
                total += len(data['readings'])
                print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                if len(data['readings']) > 0:
                    lastReadings[rID['id']] = data['readings'][0][0]
                else:
                    if not rID['id'] in lastReadings:
                        lastReadings[rID['id']] ='2017-01-01T00:00:00Z'
            pickle.dump(lastReadings, open(lastUrl, 'wb'))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # Send request to get data
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

    # Build a record in the standard format
    def buildRecord(self, item, sensor):
        record = BaseRecord()
        payload = SmartCitizenPayload()
        location = LocationRecord()

        payload.setId(sensor['id'])
        payload.setName(sensor['name'])
        payload.setState(sensor['state'])
        payload.setValue(item[1])
        payload.setDescription(sensor['description'])
        payload.setAddedAt(sensor['added_at'])

        longitude, latitude = sensor['longitude'], sensor['latitude']
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName('')
        location.setStreetNumber('')

        record.setId(str(sensor['id']) + '.' + item[0].replace(' ', ''))
        record.setSource(collectorCfg['collectors']['smartcitizen']['source_name'])
        record.setProvider(re.findall('[A-Z][^A-Z]*', sensor['user_tags'][-1])[0])
        record.setPublisher(sensor['name'])
        record.setType(re.findall('[A-Z][^A-Z]*', sensor['user_tags'][-1])[1])
        record.setTimestamp(item[0].split('T')[0]+'T'+item[0].split('T')[1].split(':')[0]+':00:00Z')
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # Save data to permanent storage
    def saveData(self, data, sensor):
        items = data
        if 'readings' in data:
            for item in reversed(data['readings']):
                StorageHelper().store(self.buildRecord(item, sensor).toJSON())
                #print(str(datetime.datetime.now()) + ' ' + '            ' + str(index+1) + ' of ' + str(len(items)) + ' Saving ' + record.toJSON())

    # Get the list of all the sensors
    def getAllSensors(self):
        flag = True
        while flag:
            try:
                flag = False
                url = 'https://api.smartcitizen.me/v0/devices/world_map'
                response = requests.get(url=url)
                data = response.json()
                return [sensor for sensor in data if 'SentiloNoise' in sensor['user_tags']]
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

if __name__ == "__main__":
    base = collectorCfg['collectors']['smartcitizen']['base_url']
    SmartCitizentCollector().start(base)