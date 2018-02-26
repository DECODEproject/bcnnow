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

# This class defines a set of utilities methods to manipulate timestamps.
class TimeHelper:

    def __init__(self):
        return

    # This method translates integer timestamp parameters into a string with format 'yyyy-mm-dd hh:mm:ss'.
    def toDate(self, year, month, day, hours='00', minutes='00', seconds='00'):
        return year + '-' + "{0:0>2}".format(month) + '-' + "{0:0>2}".format(day) + ' ' + \
               "{0:0>2}".format(hours) + ':' + "{0:0>2}".format(minutes) + ':' + "{0:0>2}".format(seconds)

    # This method translates a timestamp with slash separators to a timestamp with dash separators.
    def toDash(self, timestamp):
        if timestamp != None and timestamp != '':
            return self.toDate(timestamp.split('/')[2], timestamp.split('/')[1], timestamp.split('/')[0])
        return ''