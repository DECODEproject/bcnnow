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

# This class defines a set of configuration variables for IRIS collector.
class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "odi": {
                          "source_name": "odi",
                          "iris": {
                                      "source_name": "iris",
                                      "base_url": "http://opendata-ajuntament.barcelona.cat/collection",
                                      "api_base_url": "/api/action/datastore_search?resource_id=",
                                      "complaint_urls": ['3544d426-dda7-49ae-9378-13689113b065',
                                                          'c3acbbed-3949-4d1c-8532-9f7a2c7fc638',
                                                          '80e94972-1b4a-4162-8c7f-d4b356eb1554',
                                                          'b92e1902-de85-43ab-b438-9e1679d00886'],
                                    }
                  }
            }
        }

    def get(self):
        return self.config