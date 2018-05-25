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
sys.path.append('Insert your path to the BarcelonaNow project folder')

from apps.backend.data.collectors.pull.SentiloCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
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

# This class defines the structure of Sentilo collector which adopts the pull strategy.
class SentiloCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        lastUrl =  'history/sentilo-last-readings.pkl'
        lastReadings = pickle.load(open(lastUrl, 'rb')) if os.path.isfile(lastUrl) else {}
        url =  collectorCfg['collectors']['sentilo']['base_url'] + 'catalog/'
        providers = self.sendRequest(url, "sensors")

        print("Providers List:")
        for i, provider in enumerate(providers['providers']):
            print(i, provider['provider'])

        if 'providers' in providers:
            for provider in providers['providers']:
                print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + provider['provider'])
                for sensor in provider['sensors']:
                    print(str(datetime.datetime.now()) + ' ' + '        Collecting collection for ' + sensor['sensor'])
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

    # This method sends a request to get Sentilo data
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

    # This method builds a Sentilo BaseRecord
    def buildRecord(self, observation, provider, sensor):
        record = BaseRecord()
        payload = SentiloPayload()
        location = LocationRecord()

        payload.setValue(observation['value'])
        payload.setType(sensor['type'])
        payload.setDescription(sensor['description'])
        payload.setEmplacament(sensor['additionalInfo']['emplaçament'] if 'additionalInfo' in sensor else '')
        payload.setUnit(sensor['unit'])

        longitude, latitude = sensor['location'].split(' ')[1], sensor['location'].split(' ')[0]
        location.setPoint(latitude, longitude)
        location.setAltitude(sensor['additionalInfo']['altitud'] if 'additionalInfo' in sensor else '')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(district)
        location.setNeighbourhood(neighbourhood)
        location.setStreetName('')
        location.setStreetNumber('')

        record.setId(sensor['sensor'] + '.' + observation['timestamp'].replace(' ', ''))
        record.setSource(collectorCfg['collectors']['sentilo']['source_name'])
        record.setProvider(provider['provider'])
        record.setPublisher(sensor['sensor'])
        record.setType(sensor['componentType'])
        record.setTimestamp(observation['timestamp'])
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves a Sentilo BaseRecord
    def saveData(self, data, provider, sensor):
        StorageHelper().store(self.buildRecord(data, provider, sensor).toJSON())

if __name__ == "__main__":
    SentiloCollector().start()