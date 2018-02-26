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

from backend.data.collectors.pull.CityOsCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

# This class defines the structure of CityOS collector which adopts the pull strategy.
class CityOSCollector:

    def __init__(self, ):
        return

    # This method starts the collection process
    def start(self, base, resourceIDs=[]):
        return

    # This method sends a request to get CityOS data
    def sendRequest(self, url):
        return

    # This method builds a CityOS BaseRecord
    def buildRecord(self, item):
        return

    # This method permanently stores a CityOS BaseRecord
    def saveData(self, data):
        return

if __name__ == "__main__":
    CityOSCollector().start('', [])