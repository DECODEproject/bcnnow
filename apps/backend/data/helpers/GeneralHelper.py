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

# This class defines a set of utilities methods to validate input data.
class GeneralHelper:

    def __init__(self):
        return

    # This method checks if the string s includes at least one character
    def check(self, s):
        return s != None and s != ''

    # This method returns an empty string if s is empty or none otherwise returns s itself
    def default(self, s):
        if self.check(s):
            return s
        return ''

    # This method parses the list of categories included into each ASIA record and saves them into a dictionary
    def toClassifications(self, source):
        destination = {}
        if isinstance(source['nivell'], list):
            for classification in source['nivell']:
                class_id = classification['@codi'].lstrip('0')
                class_name = classification['#text']
                destination[class_id] = class_name
        else:
            class_id = source['nivell']['@codi'].lstrip('0')
            class_name = source['nivell']['#text']
            destination[class_id] = class_name
        return destination

    # This methods parses the list of equipments associated to a ODI point of interest and saves them into a dictionary
    def toAssociations(self, source):
        destination = {}
        if isinstance(source, list):
            for association in source:
                class_id = association['@code'].lstrip('0')
                class_name = association['@label']
                destination[class_id] = class_name
        else:
            class_id = source['@code'].lstrip('0')
            class_name = source['@label']
            destination[class_id] = class_name
        return destination

    # This method translates one-char ASIA event state into a long event state description
    def toAsiaState(self, state):
        return {'A': 'dependent', 'S': 'suspended', 'C': 'current'}[state]

    # This method translates one-char ASIA event type into a long event type description
    def toAsiaType(self, type):
        return {'P': 'punctual', 'C': 'cyclic', 'E': 'fixed'}[type]

    # This method translates one-char ASIA event state cycle into a long event state cycle description
    def toAsiaStateCycle(self, cycle):
        return {'V': 'current', 'C': 'timedout', 'L': 'latent'}[cycle]