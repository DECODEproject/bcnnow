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

from apps.backend.data.collectors.pull.InsideAirbnbCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from apps.backend.data.collectors.pull.InsideAirbnbCollector.InsideAirbnbListingPayload import InsideAirbnbListingPayload
from apps.backend.data.models.BaseRecord import BaseRecord
from apps.backend.data.helpers.StorageHelper import StorageHelper
from apps.backend.data.helpers.LocationHelper import LocationHelper
from apps.backend.data.models.LocationRecord import LocationRecord
from apps.backend.data.helpers.GeneralHelper import GeneralHelper

import pandas as pd
import datetime

# This class defines the structure of Inside Airbnb Listing collector which adopts the pull strategy.
class InsideAirbnbListingCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        total = 0
        for rindex, rID in enumerate(resourceIDs):
            print(str(datetime.datetime.now()) + ' ' + '    Collecting collection for ' + rID)
            url = base + str(rID)
            print(str(datetime.datetime.now()) + ' ' + '        ' + ' Access to URL: ' + url)
            data = self.sendRequest(url)
            self.saveData(data)
            total += len(data.index)
            print(str(datetime.datetime.now()) + ' ' + '         Total: ' + str("{0:0>9}".format(total)))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method sends a request to get Inside Airbnb Listing data
    def sendRequest(self, url):
        return pd.read_csv(url, low_memory=False)

    # This method build an Inside Airbnb Listing BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = InsideAirbnbListingPayload()
        location = LocationRecord()

        payload.setId(item['id'])
        payload.setName(item['name'])
        payload.setDescription(item['description'])
        payload.setAccess(item['access'])
        payload.setAmenities(item['amenities'])
        payload.setBathrooms(item['bathrooms'])
        payload.setBedrooms(item['bedrooms'])
        payload.setBeds(item['beds'])
        payload.setBedType(item['bed_type'])
        payload.setCalendarLastScraped(item['calendar_last_scraped'])
        payload.setCalendarUpdated(item['calendar_updated'])
        payload.setCancellationPolicy(item['cancellation_policy'])
        payload.setCleaningFee(item['cleaning_fee'])
        payload.setExperiencesOffered(item['experiences_offered'])
        payload.setExtraPeople(item['extra_people'])
        payload.setGuestsIncluded(item['guests_included'])
        payload.setHasAvailability(item['has_availability'])
        payload.setHostAbout(item['host_about'])
        payload.setHostAcceptanceRate(item['host_acceptance_rate'])
        payload.setHostHasProfilePic(item['host_has_profile_pic'])
        payload.setHostID(item['host_id'])
        payload.setListingUrl(item['listing_url'])
        payload.setScrapeID(item['scrape_id'])
        payload.setLastScraped(item['last_scraped'])
        payload.setSummary(item['summary'])
        payload.setSpace(item['space'])
        payload.setNeighbourhoodOverview(item['neighborhood_overview'])
        payload.setNotes(item['notes'])
        payload.setTransit(item['transit'])
        payload.setInteraction(item['interaction'])
        payload.setHouseRules(item['house_rules'])
        payload.setThumbnailUrl(item['thumbnail_url'])
        payload.setMediumUrl(item['medium_url'])
        payload.setPictureUrl(item['picture_url'])
        payload.setXLPictureUrl(item['xl_picture_url'])
        payload.setHostUrl(item['host_url'])
        payload.setHostName(item['host_name'])
        payload.setHostSince(item['host_since'])
        payload.setHostLocation(item['host_location'])
        payload.setHostResponseTime(item['host_response_time'])
        payload.setHostResponseRate(item['host_response_rate'])
        payload.setHostIsSuperhost(item['host_is_superhost'])
        payload.setHostThumbnailUrl(item['host_thumbnail_url'])
        payload.setHostPictureUrl(item['host_picture_url'])
        payload.setHostNeighbourhood(item['host_neighbourhood'])
        payload.setHostVerifications(item['host_verifications'])
        payload.setHostHasProfile(item['host_has_profile_pic'])
        payload.setHostIdentityVerified(item['host_identity_verified'])
        payload.setPropertyType(item['property_type'])
        payload.setRoomType(item['room_type'])
        payload.setAccomodates(item['accommodates'])
        payload.setScrapeID(item['scrape_id'])
        payload.setSquareFeet(item['square_feet'])
        payload.setPrice(item['price'])
        payload.setWeeklyPrice(item['weekly_price'])
        payload.setMonthlyPrice(item['monthly_price'])
        payload.setSecurityDeposit(item['security_deposit'])
        payload.setGuestsIncluded(item['guests_included'])
        payload.setMinimumNights(item['minimum_nights'])
        payload.setMaximumNights(item['maximum_nights'])
        payload.setCalendarUpdated(item['calendar_updated'])
        payload.setRequiresLicense(item['requires_license'])
        payload.setLicense(item['license'])
        payload.setJurisdictionNames(item['jurisdiction_names'])
        payload.setInstantBookable(item['instant_bookable'])
        payload.setRequireGuestProfilePicture(item['require_guest_profile_picture'])
        payload.setRequireGuestPhoneVerification(item['require_guest_phone_verification'])

        longitude, latitude = item['longitude'], item['latitude']
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
        record.setType(collectorCfg['collectors']['insideairbnb']['listing_source_name'])
        record.setTimestamp('2017-04-08T00:00:00Z')
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method saves an Inside Airbnb Listin BaseRecord
    def saveData(self, data):
        items = data
        if len(items.index) >= 0:
            for index, item in items.iterrows():
                StorageHelper().store(self.buildRecord(item).toJSON())

if __name__ == "__main__":
    base = collectorCfg['collectors']['insideairbnb']['base_url']
    resourceIDs = collectorCfg['collectors']['insideairbnb']['listing_urls']
    InsideAirbnbListingCollector().start(base, resourceIDs)