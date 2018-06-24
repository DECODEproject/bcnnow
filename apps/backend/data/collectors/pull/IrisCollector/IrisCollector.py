import sys
sys.path.append('/home/code/projects/decode-bcnnow/')

from apps.backend.data.collectors.pull.IrisCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.IrisCollector.IrisPayload import IrisPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.TimeHelper import TimeHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import requests

class IrisCollector:
    def __init__(self, ):
        return

    # Start reader process
    def start(self, base, resourceIDs=[]):
        # print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        for rindex, rID in enumerate(resourceIDs):
            # print(str(datetime.datetime.now()) + ' ' + '    Collecting data for ' + rID)
            url = base + collectorCfg['collectors']['odi']['iris']['api_base_url'] + str(rID) + '&offset=' + str(0)
            flag = True
            total = 0
            while flag:
                # print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
                data = self.sendRequest(url)
                self.saveData(data)
                url = base + data['result']['_links']['next']
                flag = len(data['result']['records']) > 0
                total += len(data['result']['records'])
                # print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
                # print(str(datetime.datetime.now()) + ' ' + 'End collection')

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
                # print(str(datetime.datetime.now()) + ' ' + '         Reconnecting...')
                flag = True

    # Build a record in the standard format
    def buildRecord(self, item):
        record = BaseRecord()
        payload = IrisPayload()
        location = LocationRecord()

        payload.setId(GeneralHelper().default(item['FITXA_ID']))
        payload.setArea(GeneralHelper().default(item['AREA']))
        payload.setChannel(GeneralHelper().default(item['CANALS_RESPOSTA']))
        payload.setDetail(GeneralHelper().default(item['DETALL']))
        payload.setElement(GeneralHelper().default(item['ELEMENT']))
        payload.setStartDate(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_ALTA']),
                                                 GeneralHelper().default(item['MES_DATA_ALTA']),
                                                 GeneralHelper().default(item['DIA_DATA_ALTA'])))
        payload.setEndDate(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_TANCAMENT']),
                                               GeneralHelper().default(item['MES_DATA_TANCAMENT']),
                                               GeneralHelper().default(item['DIA_DATA_TANCAMENT'])))
        payload.setSupport(GeneralHelper().default(item['SUPORT']))

        location.setPoint(item['LATITUD'], item['LONGITUD'])
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        location.setDistrict(GeneralHelper().default(item['DISTRICTE']))
        location.setNeighbourhood(GeneralHelper().default(item['BARRI']))
        location.setStreetName(
            GeneralHelper().default(item['TIPUS_VIA']) + ' ' + GeneralHelper().default(item['CARRER']))
        location.setStreetNumber(GeneralHelper().default(item['NUMERO']))

        record.setId(GeneralHelper().default(item['FITXA_ID']))
        record.setSource(collectorCfg['collectors']['odi']['iris']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(GeneralHelper().default(item['TIPUS']))
        record.setTimestamp(TimeHelper().toDate(GeneralHelper().default(item['ANY_DATA_ALTA']),
                                                GeneralHelper().default(item['MES_DATA_ALTA']),
                                                GeneralHelper().default(item['DIA_DATA_ALTA'])))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # Save data to permanent storage
    def saveData(self, data):
        items = data['result']['records']
        if len(items) >= 0:
            for index, item in enumerate(items):
                StorageHelper().store(self.buildRecord(item).toJSON())
                #print(str(datetime.datetime.now()) + ' ' + '            ' + str(index+1) + ' of ' + str(len(items)) + ' Saving ' + record.toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['odi']['iris']['base_url']
    resourceIDs = collectorCfg['collectors']['odi']['iris']['complaint_urls']
    IrisCollector().start(base, resourceIDs)

