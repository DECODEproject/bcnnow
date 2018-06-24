class GeneralHelper:

    def __init__(self):
        return

    # Check if val is valid
    def check(self, val):
        return val != None and val != ''

    # Return an empty string if val is not valid
    def default(self, val):
        if self.check(val):
            return val
        return ''

    # Parse ASIA classification categories and save them to a dictionary
    def toClassifications(self, source):
        dest = {}
        if isinstance(source['nivell'], list):
            clist = []
            for classification in source['nivell']:
                class_id = classification['@codi'].lstrip('0')
                class_name = classification['#text']
                dest[class_id] = class_name
        else:
            class_id = source['nivell']['@codi'].lstrip('0')
            class_name = source['nivell']['#text']
            dest[class_id] = class_name
        return dest

    # Parse Points of Interest associations and save them to a dictionary
    def toAssociations(self, source):
        dest = {}
        if isinstance(source, list):
            for association in source:
                class_id = association['@code'].lstrip('0')
                class_name = association['@label']
                dest[class_id] = class_name
        else:
            class_id = source['@code'].lstrip('0')
            class_name = source['@label']
            dest[class_id] = class_name
        return dest

    # Parse ASIA event state
    def toAsiaState(self, input):
        return {'A': 'dependent', 'S': 'suspended', 'C': 'current'}[input]

    # Parse ASIA event type
    def toAsiaType(self, input):
        return {'P': 'punctual', 'C': 'cyclic', 'E': 'fixed'}[input]

    # Parse ASIA event state cycle
    def toAsiaStateCycle(self, input):
        return {'V': 'current', 'C': 'timedout', 'L': 'latent'}[input]