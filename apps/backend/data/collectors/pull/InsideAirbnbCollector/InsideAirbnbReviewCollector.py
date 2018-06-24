import sys
sys.path.append('/home/code/projects/decode-bcnnow/')

from apps.backend.data.collectors.pull.InsideAirbnbCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.InsideAirbnbCollector.InsideAirbnbReviewPayload import InsideAirbnbReviewPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from apps.backend.data.helpers.StorageHelper import StorageHelper

import pandas as pd
import datetime

class InsideAirbnbReviewCollector:

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
            total += len(data.index)
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # Send request to get data
    def sendRequest(self, url):
        return pd.read_csv(url)

    # Build a record in the standard format
    def buildRecord(self, item):
        record = BaseRecord()
        payload = InsideAirbnbReviewPayload()
        location = LocationRecord()

        payload.setId(item['id'])
        payload.setListingID(item['listing_id'])
        payload.setDate(item['date'])
        payload.setComments(item['comments'])
        payload.setReviewerID(item['reviewer_id'])
        payload.setReviewerName(item['reviewer_name'])

        longitude, latitude = GeneralHelper().default(''), GeneralHelper().default('')
        location.setPoint(latitude, longitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        district, neighbourhood = LocationHelper().getLocationAreas(latitude, longitude)
        location.setDistrict(GeneralHelper().default(district))
        location.setNeighbourhood(GeneralHelper().default(neighbourhood))
        location.setStreetName(GeneralHelper().default(''))
        location.setStreetNumber(GeneralHelper().default(''))

        record.setId(item['id'])
        record.setSource(collectorCfg['collectors']['insideairbnb']['source_name'])
        record.setProvider('')
        record.setPublisher('')
        record.setType(collectorCfg['collectors']['insideairbnb']['review_source_name'])
        record.setTimestamp(str(datetime.datetime.now()))
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # Save data to permanent storage
    def saveData(self, data):
        items = data
        if len(items.index) >= 0:
            for index, item in items.iterrows():
                StorageHelper().store(self.buildRecord(item).toJSON())
                #print(str(datetime.datetime.now()) + ' ' + '            ' + str(index+1) + ' of ' + str(len(items)) + ' Saving ' + record.toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['insideairbnb']['base_url']
    resourceIDs = collectorCfg['collectors']['insideairbnb']['review_urls']
    InsideAirbnbReviewCollector().start(base, resourceIDs)