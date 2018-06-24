import json

class IrisPayload:

    def __init__(self):
        self.irisID = ''
        self.area = ''
        self.element = ''
        self.detail = ''
        self.support = ''
        self.channel = ''
        self.startDate = ''
        self.endDate = ''

    def setId(self, irisid):
        self.irisID = irisid

    def setArea(self, area):
        self.area = area.title()

    def setElement(self, element):
        self.element = element.title()

    def setDetail(self, detail):
        self.detail = detail.title()

    def setSupport(self, support):
        self.support = support.title()

    def setChannel(self, channel):
        self.channel = channel.title()

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    def getId(self):
        return self.irisID

    def getArea(self):
        return self.area

    def getElement(self):
        return self.element

    def getDetail(self):
        return self.detail

    def getSupport(self):
        return self.support

    def getChannel(self):
        return self.channel

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def toJSON(self):
        return '{'    +\
                  '"id": ' + json.dumps(self.getId()) +','  +\
                  '"area": ' + json.dumps(self.getArea()) +','  +\
                  '"element": ' + json.dumps(self.getElement()) +','  +\
                  '"detail": ' + json.dumps(self.getDetail()) +','  +\
                  '"support": ' + json.dumps(self.getSupport()) +','  +\
                  '"channel": ' + json.dumps(self.getChannel()) +','  +\
                  '"startdate": ' + json.dumps(self.getStartDate()) +',' +\
                  '"enddate": ' + json.dumps(self.getEndDate()) + ''  +\
               '}'