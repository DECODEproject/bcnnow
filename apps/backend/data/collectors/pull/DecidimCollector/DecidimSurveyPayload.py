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

# This class defines the structure of the payload field for an instance of a Decidim Proposal.
class DecidimSurveyPayload:

    def __init__(self):
        self.id = ''
        self.gender = ''
        self.age = ''
        self.country = ''
        self.continent = ''
        self.education = ''
        self.workSituation = ''
        self.organization = ''
        self.city = ''
        self.district = ''
        self.device = ''
        self.scale = ''
        self.interest = ''         


    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id


    def setGender(self, gender):
        self.gender = gender

    def getGender(self):
        return self.gender 


    def setAge(self, age):
        self.age = age

    def getAge(self):
        return self.age        


    def setCountry(self, country):
        self.country = country

    def getCountry(self):
        return self.country        


    def setContinent(self, continent):
        self.continent = continent

    def getContinent(self):
        return self.continent        


    def setEducation(self, education):
        self.education = education

    def getEducation(self):
        return self.education        


    def setWorkSituation(self, workSituation):
        self.workSituation = workSituation

    def getWorkSituation(self):
        return self.workSituation        


    def setOrganization(self, organization):
        self.organization = organization

    def getOrganization(self):
        return self.organization        


    def setCity(self, city):
        self.city = city

    def getCity(self):
        return self.city        


    def setDistrict(self, district):
        self.district = district

    def getDistrict(self):
        return self.district        


    def setDevice(self, device):
        self.device = device

    def getDevice(self):
        return self.device        


    def setScale(self, scale):
        self.scale = scale

    def getScale(self):
        return self.scale        


    def setInterest(self, interest):
        self.interest = interest

    def getInterest(self):
        return self.interest        


    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId())  +','  +\
                  '"gender": ' + json.dumps(self.getGender())  +','  +\
                  '"age": ' + json.dumps(self.getAge())  +','  +\
                  '"country": ' + json.dumps(self.getCountry())  +','  +\
                  '"continent": ' + json.dumps(self.getContinent())  +','  +\
                  '"education": ' + json.dumps(self.getEducation())  +','  +\
                  '"workSituation": ' + json.dumps(self.getWorkSituation())  +','  +\
                  '"organization": ' + json.dumps(self.getOrganization())  +','  +\
                  '"city": ' + json.dumps(self.getCity())  +','  +\
                  '"district": ' + json.dumps(self.getDistrict())  +','  +\
                  '"device": ' + json.dumps(self.getDevice())  +','  +\
                  '"scale": ' + json.dumps(self.getScale())  +','  +\
                  '"interest": ' + json.dumps(self.getInterest())  +\
               '}'
