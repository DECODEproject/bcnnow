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

import json

# This class defines the structure of the payload field for an instance of an Inside Airbnb Listing BaseRecord.
class InsideAirbnbListingPayload:

    def __init__(self):
        self.id = ''
        self.listingUrl = ''
        self.name = ''
        self.summary = ''
        self.space = ''
        self.description = ''
        self.experiencesOffered = ''
        self.neighborhoodOverview = ''
        self.notes = ''
        self.transit = ''
        self.access = ''
        self.interaction = ''
        self.houseRules = ''

        self.thumbnailUrl = ''
        self.mediumUrl = ''
        self.pictureUrl = ''
        self.xlPictureUrl = ''

        self.hostID = ''
        self.hostUrl = ''
        self.hostName = ''
        self.hostSince = ''
        self.hostLocation = ''
        self.hostAbout = ''
        self.hostResponseTime = ''
        self.hostResponseRate = ''
        self.hostAcceptanceRate = ''
        self.hostIsSuperhost = ''
        self.hostThumbnailUrl = ''
        self.hostPictureUrl = ''
        self.hostNeighbourhood = ''
        self.hostVerifications = ''
        self.hostHasProfilePic = ''
        self.hostHasProfile = ''
        self.hostIdentityVerified = ''

        self.price = 0
        self.weeklyPrice = 0
        self.monthlyPrice = 0
        self.securityDeposit = 0
        self.cleaningFee = 0

        self.guestsIncluded = ''
        self.extraPeople = ''
        self.minimumNights = ''
        self.maximumNights = ''
        self.calendarUpdated = ''
        self.hasAvailability = ''
        self.requiresLicense = ''
        self.license = ''
        self.jurisdictionNames = ''
        self.instantBookable = ''
        self.cancellationPolicy = ''
        self.requireGuestProfilePicture = ''
        self.requireGuestPhoneVerification = ''

        self.scrapeID = ''
        self.lastScraped = ''
        self.calendarLastScraped = ''

    def setId(self, id):
        self.id = str(id)

    def setListingUrl(self, listingUrl):
        self.listingUrl = str(listingUrl)

    def setScrapeID(self, scrapeID):
        self.scrapeID = str(scrapeID)

    def setLastScraped(self, lastScraped):
        self.lastScraped = str(lastScraped)

    def setName(self, name):
        self.name = str(name)

    def setSummary(self, summary):
        self.summary = str(summary)

    def setSpace(self, space):
        self.space = str(space)

    def setDescription(self, description):
        self.description = str(description)

    def setExperiencesOffered(self, experiencesoffered):
        self.experiencesOffered = str(experiencesoffered)

    def setNeighbourhoodOverview(self, neighbourhoodOverview):
        self.neighborhoodOverview = str(neighbourhoodOverview)

    def setNotes(self, notes):
        self.notes = str(notes)

    def setTransit(self, transit):
        self.transit = str(transit)

    def setAccess(self, access):
        self.access = str(access)

    def setInteraction(self, interaction):
        self.interaction = str(interaction)

    def setHouseRules(self, houseRules):
        self.houseRules = str(houseRules)

    def setThumbnailUrl(self, thumbnailUrl):
        self.thumbnailUrl = str(thumbnailUrl)

    def setMediumUrl(self, mediumUrl):
        self.mediumUrl = str(mediumUrl)

    def setPictureUrl(self, pictureUrl):
        self.pictureUrl = str(pictureUrl)

    def setXLPictureUrl(self, xlPictureUrl):
        self.xlPictureUrl = str(xlPictureUrl)

    def setHostID(self, hostID):
        self.hostID = str(hostID)

    def setHostUrl(self, hostUrl):
        self.hostUrl = str(hostUrl)

    def setHostName(self, hostName):
        self.hostName = str(hostName)

    def setHostSince(self, hostSince):
        self.hostSince = str(hostSince)

    def setHostLocation(self, hostLocation):
        self.hostLocation = str(hostLocation)

    def setHostAbout(self, hostAbout):
        self.hostAbout = str(hostAbout)

    def setHostResponseTime(self, hostResponseTime):
        self.hostResponseTime = str(hostResponseTime)

    def setHostResponseRate(self, hostResponseRate):
        self.hostResponseRate = str(hostResponseRate)

    def setHostAcceptanceRate(self, hostAcceptanceRate):
        self.hostAcceptanceRate = str(hostAcceptanceRate)

    def setHostIsSuperhost(self, hostIsSuperhost):
        self.hostIsSuperhost = str(hostIsSuperhost)

    def setHostThumbnailUrl(self, hostThumbnailUrl):
        self.hostThumbnailUrl = str(hostThumbnailUrl)

    def setHostPictureUrl(self, hostPictureUrl):
        self.hostPictureUrl = str(hostPictureUrl)

    def setHostNeighbourhood(self, hostNeighbourhood):
        self.hostNeighbourhood = str(hostNeighbourhood)

    def setHostVerifications(self, hostVerifications):
        self.hostVerifications = str(hostVerifications)

    def setHostHasProfilePic(self, hostHasProfilePic):
        self.hostHasProfilePic = str(hostHasProfilePic)

    def setHostHasProfile(self, hostHasProfile):
        self.hostHasProfile = str(hostHasProfile)

    def setHostIdentityVerified(self, hostIdentityVerified):
        self.hostIdentityVerified = str(hostIdentityVerified)

    def setPropertyType(self, propertyType):
        self.propertyType = str(propertyType)

    def setRoomType(self, roomType):
        self.roomType = str(roomType)

    def setAccomodates(self, accommodates):
        self.accommodates = str(accommodates)

    def setBathrooms(self, bathrooms):
        self.bathrooms = str(bathrooms)

    def setBedrooms(self, bedrooms):
        self.bedrooms = str(bedrooms)

    def setBeds(self, beds):
        self.beds = str(beds)

    def setBedType(self, bedType):
        self.bedType = str(bedType)

    def setAmenities(self, amenities):
        self.amenities = str(amenities)

    def setSquareFeet(self, squareFeet):
        self.squareFeet = str(squareFeet)

    def setPrice(self, price):
        self.price = float(price)

    def setWeeklyPrice(self, weeklyPrice):
        self.weeklyPrice = float(weeklyPrice)

    def setMonthlyPrice(self, monthlyPrice):
        self.monthlyPrice = float(monthlyPrice)

    def setSecurityDeposit(self, securityDeposit):
        self.securityDeposit = float(securityDeposit)

    def setCleaningFee(self, cleaningFee):
        self.cleaningFee = float(cleaningFee)

    def setGuestsIncluded(self, guestsIncluded):
        self.guestsIncluded = str(guestsIncluded)

    def setExtraPeople(self, extraPeople):
        self.extraPeople = str(extraPeople)

    def setMinimumNights(self, minimumNights):
        self.minimumNights = str(minimumNights)

    def setMaximumNights(self, maximumNights):
        self.maximumNights = str(maximumNights)

    def setCalendarUpdated(self, calendarUpdated):
        self.calendarUpdated = str(calendarUpdated)

    def setHasAvailability(self, hasAvailability):
        self.hasAvailability = str(hasAvailability)

    def setCalendarLastScraped(self, calendarLastScraped):
        self.calendarLastScraped = str(calendarLastScraped)

    def setRequiresLicense(self, requiresLicense):
        self.requiresLicense = str(requiresLicense)

    def setLicense(self, license):
        self.license = str(license)

    def setJurisdictionNames(self, jurisdictionNames):
        self.jurisdictionNames = str(jurisdictionNames)

    def setInstantBookable(self, instantBookable):
        self.instantBookable = str(instantBookable)

    def setCancellationPolicy(self, cancellationPolicy):
        self.cancellationPolicy = str(cancellationPolicy)

    def setRequireGuestProfilePicture(self, requireGuestProfilePicture):
        self.requireGuestProfilePicture = str(requireGuestProfilePicture)

    def setRequireGuestPhoneVerification(self, requireGuestPhoneVerification):
        self.requireGuestPhoneVerification = str(requireGuestPhoneVerification)

    def getId(self):
        return self.id

    def getListingUrl(self):
        return self.listingUrl

    def getScrapeID(self):
        return self.scrapeID

    def getLastScraped(self):
        return self.lastScraped

    def getName(self):
        return self.name

    def getSummary(self):
        return self.summary

    def getSpace(self):
        return self.space

    def getDescription(self):
        return self.description

    def getExperiencesOffered(self):
        return self.experiencesOffered

    def getNeighbourhoodOverview(self):
        return self.neighborhoodOverview

    def getNotes(self):
        return self.notes

    def getTransit(self):
        return self.transit

    def getAccess(self):
        return self.access

    def getInteraction(self):
        return self.interaction

    def getHouseRules(self):
        return self.houseRules

    def getThumbnailUrl(self):
        return self.thumbnailUrl

    def getMediumUrl(self):
        return self.mediumUrl

    def getPictureUrl(self):
        return self.pictureUrl

    def getXLPictureUrl(self):
        return self.xlPictureUrl

    def getHostID(self):
        return self.hostID

    def getHostUrl(self):
        return self.hostUrl

    def getHostName(self):
        return self.hostName

    def getHostSince(self):
        return self.hostSince

    def getHostLocation(self):
        return self.hostLocation

    def getHostAbout(self):
        return self.hostAbout

    def getHostResponseTime(self):
        return self.hostResponseTime

    def getHostResponseRate(self):
        return self.hostResponseRate

    def getHostAcceptanceRate(self):
        return self.hostAcceptanceRate

    def getHostIsSuperhost(self):
        return self.hostIsSuperhost

    def getHostThumbnailUrl(self):
        return self.hostThumbnailUrl

    def getHostPictureUrl(self):
        return self.hostPictureUrl

    def getHostNeighbourhood(self):
        return self.hostNeighbourhood

    def getHostVerifications(self):
        return self.hostVerifications

    def getHostHasProfilePic(self):
        return self.hostHasProfilePic

    def getHostHasProfile(self):
        return self.hostHasProfile

    def getHostIdentityVerified(self):
        return self.hostIdentityVerified

    def getPropertyType(self):
        return self.propertyType

    def getRoomType(self):
        return self.roomType

    def getAccomodates(self):
        return self.accommodates

    def getBathrooms(self):
        return self.bathrooms

    def getBedrooms(self):
        return self.bedrooms

    def getBeds(self):
        return self.beds

    def getBedType(self):
        return self.bedType

    def getAmenities(self):
        return self.amenities

    def getSquareFeet(self):
        return self.squareFeet

    def getPrice(self):
        return self.price

    def getWeeklyPrice(self):
        return self.weeklyPrice

    def getMonthlyPrice(self):
        return self.monthlyPrice

    def getSecurityDeposit(self):
        return self.securityDeposit

    def getCleaningFee(self):
        return self.cleaningFee

    def getGuestsIncluded(self):
        return self.guestsIncluded

    def getExtraPeople(self):
        return self.extraPeople

    def getMinimumNights(self):
        return self.minimumNights

    def getMaximumNights(self):
        return self.maximumNights

    def getCalendarUpdated(self):
        return self.calendarUpdated

    def getHasAvailability(self):
        return self.hasAvailability

    def getCalendarLastScraped(self):
        return self.calendarLastScraped

    def getRequiresLicense(self):
        return self.requiresLicense

    def getLicense(self):
        return self.license

    def getJurisdictionNames(self):
        return self.jurisdictionNames

    def getInstantBookable(self):
        return self.instantBookable

    def getCancellationPolicy(self):
        return self.cancellationPolicy

    def getRequireGuestProfilePicture(self):
        return self.requireGuestProfilePicture

    def getRequireGuestPhoneVerification(self):
        return self.requireGuestPhoneVerification

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"listingurl": ' + json.dumps(self.getListingUrl()) +','  +\
                  '"scrapeid": ' + json.dumps(self.getScrapeID()) +','  +\
                  '"lastscraped": ' + json.dumps(self.getLastScraped()) +','  +\
                  '"name": ' + json.dumps(self.getName()) +','  +\
                  '"summary": ' + json.dumps(self.getSummary()) +','  +\
                  '"space": ' + json.dumps(self.getSpace()) +','  +\
                  '"description": ' + json.dumps(self.getDescription()) +','  +\
                  '"experiencesoffered": ' + json.dumps(self.getExperiencesOffered()) +','  +\
                  '"neighbourhoodoverview": ' + json.dumps(self.getNeighbourhoodOverview()) +','  +\
                  '"notes": ' + json.dumps(self.getNotes()) +','  +\
                  '"transit": ' + json.dumps(self.getTransit()) +','  +\
                  '"access": ' + json.dumps(self.getAccess()) +','  +\
                  '"interaction": ' + json.dumps(self.getInteraction()) +','  +\
                  '"houserules": ' + json.dumps(self.getHouseRules()) +','  +\
                  '"thumbnailurl": ' + json.dumps(self.getThumbnailUrl()) +','  +\
                  '"mediumurl": ' + json.dumps(self.getMediumUrl()) +','  +\
                  '"pictureurl": ' + json.dumps(self.getPictureUrl()) +','  +\
                  '"xlpictureurl": ' + json.dumps(self.getXLPictureUrl()) +','  +\
                  '"hostid": ' + json.dumps(self.getHostID()) +','  +\
                  '"hosturl": ' + json.dumps(self.getHostUrl()) +','  +\
                  '"hostname": ' + json.dumps(self.getHostName()) +','  +\
                  '"hostsince": ' + json.dumps(self.getHostSince()) +','  +\
                  '"hostlocation": ' + json.dumps(self.getHostLocation()) +','  +\
                  '"hostabout": ' + json.dumps(self.getHostAbout()) +','  +\
                  '"hostresponsetime": ' + json.dumps(self.getHostResponseTime()) +','  +\
                  '"hostresponserate": ' + json.dumps(self.getHostResponseRate()) +','  +\
                  '"hostissuperhost": ' + json.dumps(self.getHostIsSuperhost()) +','  +\
                  '"hostthumbnailurl": ' + json.dumps(self.getHostThumbnailUrl()) +','  +\
                  '"hostpictureurl": ' + json.dumps(self.getHostPictureUrl()) +','  +\
                  '"hostneighbourhood": ' + json.dumps(self.getHostNeighbourhood()) +','  +\
                  '"hostverifications": ' + json.dumps(self.getHostVerifications()) +','  +\
                  '"hosthasprofilepic": ' + json.dumps(self.getHostHasProfilePic()) +','  +\
                  '"hosthasprofile": ' + json.dumps(self.getHostHasProfile()) +','  +\
                  '"hostidentityverified": ' + json.dumps(self.getHostIdentityVerified()) +','  +\
                  '"propertytype": ' + json.dumps(self.getPropertyType()) +','  +\
                  '"roomtype": ' + json.dumps(self.getRoomType()) +','  +\
                  '"accomodates": ' + json.dumps(self.getAccomodates()) +','  +\
                  '"bathrooms": ' + json.dumps(self.getBathrooms()) +','  +\
                  '"bedrooms": ' + json.dumps(self.getBedrooms()) +','  +\
                  '"beds": ' + json.dumps(self.getBeds()) +','  +\
                  '"amenities": ' + json.dumps(self.getAmenities()) +','  +\
                  '"price": ' + json.dumps(self.getPrice()) +','  +\
                  '"weeklyprice": ' + json.dumps(self.getWeeklyPrice()) +','  +\
                  '"monthlyprice": ' + json.dumps(self.getMonthlyPrice()) +','  +\
                  '"securitydeposit": ' + json.dumps(self.getSecurityDeposit()) +','  +\
                  '"cleaningfee": ' + json.dumps(self.getCleaningFee()) +','  +\
                  '"guestsincluded": ' + json.dumps(self.getGuestsIncluded()) +','  +\
                  '"extrapeople": ' + json.dumps(self.getExtraPeople()) +','  +\
                  '"minimumnights": ' + json.dumps(self.getMinimumNights()) +','  +\
                  '"maximumnights": ' + json.dumps(self.getMaximumNights()) +','  +\
                  '"hasavailability": ' + json.dumps(self.getHasAvailability()) +','  +\
                  '"calendarupdated": ' + json.dumps(self.getCalendarUpdated()) +','  +\
                  '"requireslicense": ' + json.dumps(self.getRequiresLicense()) +','  +\
                  '"license": ' + json.dumps(self.getLicense()) +','  +\
                  '"jurisdictionnames": ' + json.dumps(self.getJurisdictionNames()) +','  +\
                  '"instantbookable": ' + json.dumps(self.getInstantBookable()) +','  +\
                  '"cancellationpolicy": ' + json.dumps(self.getCancellationPolicy()) +','  +\
                  '"requireguestprofilepicture": ' + json.dumps(self.getRequireGuestProfilePicture()) +','  +\
                  '"requireguestphoneverification": ' + json.dumps(self.getRequireGuestPhoneVerification()) + '' +\
               '}'