class TimeHelper():

    def __init__(self):
        return

    # Convert date parameters in date string
    def toDate(self, year, month, day, hours='00', minutes='00', seconds='00'):
        return year + '-' + "{0:0>2}".format(month) + '-' + "{0:0>2}".format(day) + ' ' + \
               "{0:0>2}".format(hours) + ':' + "{0:0>2}".format(minutes) + ':' + "{0:0>2}".format(seconds)

    # Convert string parameter in date
    def toDash(self, slash):
        if slash != None and slash != '':
            return self.toDate(slash.split('/')[2], slash.split('/')[1], slash.split('/')[0])
        return ''