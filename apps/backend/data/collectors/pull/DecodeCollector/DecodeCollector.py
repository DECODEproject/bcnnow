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

from apps.backend.data.collectors.pull.DecodeCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

# This class defines the structure of DECODE collector which adopts the pull strategy.
class DecodeCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        return

    # This method sends a request to get DECODE data
    def sendRequest(self, url):
        return

    # This method builds a DECODE BaseRecord
    def buildRecord(self, item):
        return

    # This method permanently stores a DECODE BaseRecord
    def saveData(self, data):
        return

if __name__ == "__main__":
    DecodeCollector().start('', [])