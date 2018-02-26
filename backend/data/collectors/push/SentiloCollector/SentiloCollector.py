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

from backend.data.collectors.pull.SentiloCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()

from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

from backend.data.collectors.pull.SentiloCollector.SentiloPayload import SentiloPayload
from backend.data.models.BaseRecord import BaseRecord
from backend.data.models.LocationRecord import LocationRecord
from backend.data.helpers.StorageHelper import StorageHelper

from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json
import requests

# This class defines the server which continuously listens to Sentilo pushes.
class SentiloServer(BaseHTTPRequestHandler):

    # This method parses the GET requests and returns an error bacause only POST requests are allowed
    def do_GET(self):
        self.send_response(500)

    # This method parses the POST request pushed by the Sentilo platform
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        SentiloCollector().saveData(json.loads(data.decode('utf-8')))
        self.send_response(200)

# This class defines the structure of Sentilo collector which adopts the push strategy.
class SentiloCollector:

    def __init__(self, ):
        return

    # This method starts the server
    def start(self):
        print(str(datetime.datetime.now()) + ' ' + 'Start collection')
        print(str(datetime.datetime.now()) + ' ' + '    Server Starts %s:%s' % (collectorCfg['tokens']['sentilo']['endpoint']['private_ipa'], int(collectorCfg['tokens']['sentilo']['endpoint']['port'])))
        server = HTTPServer(("", collectorCfg['tokens']['sentilo']['endpoint']['port']), SentiloServer)
        server.serve_forever()
        server.server_close()
        print(str(datetime.datetime.now()) + ' ' + '    Server Stops %s:%s' % (collectorCfg['tokens']['sentilo']['endpoint']['private_ip'], int(collectorCfg['tokens']['sentilo']['endpoint']['port'])))
        print(str(datetime.datetime.now()) + ' ' + 'End collection')

    # This method performs the subscriptions to all the providers in Sentilo listed into the configuration variable
    def subscribe(self):
        for provider in collectorCfg['collectors']['sentilo']['providers']:
            url = collectorCfg['collectors']['sentilo']['base_url'] + 'subscribe/collection/' + provider
            data = {"endpoint": collectorCfg['tokens']['sentilo']['endpoint']['protocol'] + '://' + collectorCfg['tokens']['sentilo']['endpoint']['public_ip'] + ':' + str(collectorCfg['tokens']['sentilo']['endpoint']['port'])}
            headers = {"IDENTITY_KEY": collectorCfg['tokens']['sentilo']['production_token'], "Content-Type": "application/json"}
            print(requests.put(url, data=json.dumps(data), headers=headers).text)

    # This method builds a Sentilo BaseRecord
    def buildRecord(self, item):
        record = BaseRecord()
        payload = SentiloPayload()
        location = LocationRecord()

        payload.setValue(item['message'])

        sensor = SentiloCollector().retrieve(item['sensor'])
        longitude, latitude = sensor['location'][0] if 'location' in sensor else '', sensor['location'][1] if 'location' in sensor else ''
        location.setLongitude(longitude)
        location.setLatitude(latitude)
        location.setAltitude('0.0')
        location.setCity('Barcelona')
        location.setDistrict('')
        location.setNeighbourhood('')
        location.setStreetName('')
        location.setStreetNumber('')

        record.setSource('sentilo')
        record.setProvider(item['provider'])
        record.setPublisher(item['publisher'])
        record.setType(item['type'])
        record.setTimestamp(item['timestamp'])
        record.setLocation(location)
        record.setPayload(payload)

        return record

    # This method permanently stores a Sentilo BaseRecord
    def saveData(self, data):
        StorageHelper().store(self.buildRecord(data).toJSON())

    # This method retrieves all the active subscriptions in Sentilo
    def activeSubscriptions(self):
        url = collectorCfg['collectors']['sentilo']['base_url'] + 'subscribe/'
        data = {}
        headers = {'IDENTITY_KEY': collectorCfg['tokens']['sentilo']['production_token'], "Content-Type": "application/json"}
        response = requests.get(url, data=json.dumps(data), headers=headers)
        print(response.json())

if __name__ == "__main__":
    SentiloCollector().subscribe()
    SentiloCollector().start()