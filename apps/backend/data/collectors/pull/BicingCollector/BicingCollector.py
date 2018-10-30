import sys

from apps.backend.data.collectors.pull.BicingCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.BicingCollector.BicingPayload import BicingPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests

class BicingCollector:

    def __init__(self, ):
        return

    # Start reader process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        url = base
        print(str(datetime.datetime.now()) + ' ' + '    ' + ' Access to URL: ' + url)
        data = self.sendRequest(url)
        self.saveData(data)
        total += len(data['stations'])
        print(str(datetime.datetime.now()) + ' ' + '     Total: ' + str("{0:0>9}".format(total)))
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
    def buildRecord(self, item, start_date):
        record = BaseRecord()
        payload = BicingPayload()
        location = LocationRecord()

        payload.setId(item['id'])
        payload.setSlots(item['slots'])
        payload.setNearbyStationIDs([station for station in item['nearbyStations'].split(' ')])
        payload.setBikes(item['bikes'])
        payload.setType(item['type'])
        payload.setStatus(item['status'])

        longitude, latitude = GeneralHelper().default(item['longitude']), GeneralHelper().default(item['latitude'])
        location.setPoint(latitude, longitude)
        location.setAltitude(GeneralHelper().default(item['altitude']))
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(item['streetName']))
        location.setStreetNumber(GeneralHelper().default(item['streetNumber']))

        record.setId(item['id'] + '.' + start_date)
        record.setSource(collectorCfg['collectors']['odi']['bicing']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['odi']['bicing']['source_name'])
        record.setTimestamp(start_date)
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # Save data to permanent storage
    def saveData(self, data):
        start_date = str(datetime.datetime.now())
        items = data['stations']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item, start_date).toJSON())
                #print(str(datetime.datetime.now()) + ' ' + '            ' + str(index+1) + ' of ' + str(len(items)) + ' Saving ' + record.toJSON())


if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['bicing']['base_url']
    BicingCollector().start(base)