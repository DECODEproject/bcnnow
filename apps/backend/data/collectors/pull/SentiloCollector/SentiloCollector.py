import sys


from apps.backend.data.collectors.pull.SentiloCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.SentiloCollector.SentiloPayload import SentiloPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.StorageHelper import StorageHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper

import requests
import pickle
import datetime
import os

class SentiloCollector:

    def __init__(self, ):
        return

    # Start reader process
    def start(self):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        lastUrl =  globalCfg['project']['base_url'] + 'apps/backend/data/collectors/pull/SentiloCollector/history/sentilo-last-readings.pkl'
        lastReadings = pickle.load(open(lastUrl, 'rb')) if os.path.isfile(lastUrl) else {}
        url =  collectorCfg['collectors']['sentilo']['base_url'] + 'catalog/'
        providers = self.sendRequest(url, "sensors")
        if 'providers' in providers:
            for provider in providers['providers']:
                if provider['provider']=='CESVA':
                    print(str(datetime.datetime.now()) + ' ' + '    Collecting data for ' + provider['provider'])
                    for sensor in provider['sensors']:
                        print(str(datetime.datetime.now()) + ' ' + '        Collecting data for ' + sensor['sensor'])
                        start = lastReadings[sensor['sensor']] if sensor['sensor'] in lastReadings else '01/01/2017T00:00:00'
                        a = datetime.datetime.strptime(start, '%d/%m/%YT%H:%M:%S')
                        b = datetime.timedelta(minutes=1)
                        lastReading = (a + b).strftime("%d/%m/%YT%H:%M:%S")
                        url = collectorCfg['collectors']['sentilo']['base_url'] + 'data/' + provider['provider'] + '/' + sensor['sensor'] + '?' + 'limit=100000&from=' + lastReading
                        for observation in reversed(self.sendRequest(url, "observations")['observations']):
                            self.saveData(observation, provider, sensor)
                            lastReading = observation['timestamp']
                        if lastReading != None:
                            lastReadings[sensor['sensor']] = lastReading
                        else:
                            if not sensor['sensor'] in lastReadings:
                                lastReadings[sensor['sensor']] = '2017-01-01T00:00:00Z'
                    pickle.dump(lastReadings, open(lastUrl, 'wb'))
            print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # Send request to get data
    def sendRequest(self, url, type):
        flag = True
        while flag:
            try:
                flag = False
                headers = {"IDENTITY_KEY": collectorCfg['tokens']['sentilo']['production_token'], "Content-Type": "application/json"}
                if type == "sensors":
                    data = requests.get(url, headers=headers).json()
                elif type == "observations":
                    data = requests.get(url, headers=headers).json()
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # Build a record in the standard format
    def buildRecord(self, observation, provider, sensor):
        record = BaseRecord()
        payload = SentiloPayload()
        location = LocationRecord()

        payload.setId(sensor['sensor'])
        payload.setValue(observation['value'])
        payload.setType(sensor['type'])
        payload.setDescription(sensor['description'] if 'description' in sensor else '')
        payload.setEmplacament(sensor['additionalInfo']['emplaçament'] if ('additionalInfo' in sensor and 'emplaçament' in sensor['additionalInfo']) else '')
        payload.setUnit(sensor['unit'])

        longitude, latitude = sensor['location'].split(' ')[1], sensor['location'].split(' ')[0]
        location.setPoint(latitude, longitude)
        location.setAltitude(sensor['additionalInfo']['altitud'] if ('additionalInfo' in sensor and 'altitud' in sensor['additionalInfo']) else '')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(district)
        location.setNeighbourhood(neighbourhood)
        location.setStreetName('')
        location.setStreetNumber('')

        record.setId(sensor['sensor'] + '.' + datetime.datetime.strptime(observation['timestamp'], '%d/%m/%YT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S').replace(' ', ''))
        #record.setSource(collectorCfg['collectors']['sentilo']['source_name'])
        record.setSource('sentilo')
        record.setProvider(provider['provider'])
        record.setPublisher(sensor['sensor'])
        record.setType(sensor['componentType'])
        record.setTimestamp(datetime.datetime.strptime(observation['timestamp'], '%d/%m/%YT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S'))
        record.setLocation(location)
        record.setPayload(payload)
        print(str(datetime.datetime.now()) + ' ' + '            ' + record.toJSON())
        return record

    # Save data to permanent storage
    def saveData(self, data, provider, sensor):
        if (sensor['type']=='noise'):
            try:
                StorageHelper().store(self.buildRecord(data, provider, sensor).toJSON())
            except Exception as e:
                print(str(datetime.datetime.now()) + ' ERROR ' + str(e))
        #print(str(datetime.datetime.now()) + ' ' + '            ' + record.toJSON())

if __name__ == "__main__":
    SentiloCollector().start()

