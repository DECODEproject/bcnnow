import sys
sys.path.append('/home/rohit.kumar/Documents/Projects/Decode/code/bcnnow')

from apps.backend.data.collectors.pull.AsiaCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.AsiaCollector.AsiaEventPayload import AsiaEventPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.TimeHelper import TimeHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import datetime
import requests
import xmltodict

class AsiaEventCollector:

    def __init__(self, ):
        return

    # Start reader process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting data for ' + rID)
            url = base + str(rID)
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data)
            total += len(data['response']['body']['resultat']['actes']['acte'])
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # Send request to get data
    def sendRequest(self, url):
        flag = True
        while flag:
            try:
                flag = False
                response = requests.get(url=url)
                data = xmltodict.parse(response.text)
                return data
            except:
                print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # Build a record in the standard format
    def buildRecord(self, item):
        record = BaseRecord()
        payload = AsiaEventPayload()
        location = LocationRecord()

        payload.setName(GeneralHelper().default(item['nom']))
        payload.setEventType(GeneralHelper().toAsiaType(item['tipus_acte']))
        payload.setStartDate(TimeHelper().toDash(item['data']['data_inici']))
        payload.setEndDate(TimeHelper().toDash(item['data']['data_fi']))
        payload.setEquipmentID(GeneralHelper().default(item['lloc_simple']['id'] if 'id' in item['lloc_simple'] else ''))
        payload.setState(GeneralHelper().toAsiaState(item['estat']))
        payload.setStateCycle(GeneralHelper().toAsiaStateCycle(item['estat_cicle']))
        payload.setCategories(GeneralHelper().toClassifications(item['classificacions']))

        longitude, latitude = LocationHelper().toWGS84(GeneralHelper().default(item['lloc_simple']['adreca_simple']['coordenades']['geocodificacio']['@y']), GeneralHelper().default(item['lloc_simple']['adreca_simple']['coordenades']['geocodificacio']['@x']))
        try:
            location.setPoint(latitude, longitude)
            location.setAltitude('0.0')
            location.setCity('Barcelona')

            district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
            location.setDistrict(GeneralHelper().default(district))
            location.setNeighbourhood(GeneralHelper().default(neighbourhood))
            location.setStreetName(GeneralHelper().default(
                item['lloc_simple']['adreca_simple']['carrer']['#text'] if '#text' in
                                                                           item['lloc_simple']['adreca_simple'][
                                                                               'carrer'] else ''))
            location.setStreetNumber(GeneralHelper().default(
                item['lloc_simple']['adreca_simple']['numero']['@enter'] if '@enter' in
                                                                            item['lloc_simple']['adreca_simple'][
                                                                                'numero'] else ''))

            record.setId(GeneralHelper().default(item['id']))
            record.setSource(collectorCfg['collectors']['odi']['asia']['source_name'])
            record.setProvider('')
            record.setPublisher('')
            record.setType('event')
            record.setTimestamp(TimeHelper().toDash(item['data']['data_inici']))
            record.setLocation(location)
            record.setPayload(payload)
        except ValueError:
                return None




        return record

    # Save data to permanent storage
    def saveData(self, data):
        items = data['response']['body']['resultat']['actes']['acte']
        if len(items) >= 0:
            for index, item in enumerate(items):
                record=self.buildRecord(item)
                if(record is not None):
                    StorageHelper().store(record.toJSON())
                #print(str(datetime.datetime.now()) + ' ' + '            ' + str(index+1) + ' of ' + str(len(items)) + ' Saving ' + record.toJSON())


if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['asia']['petition_base_url']
    resourceIDs = collectorCfg['collectors']['odi']['asia']['petition_urls']
    AsiaEventCollector().start(base, resourceIDs)