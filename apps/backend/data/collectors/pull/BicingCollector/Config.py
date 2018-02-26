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


# This class defines a set of configuration variables for Bicing collector.
class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "odi": {
                              "source_name": "odi",
                              "bicing": {
                                        "source_name": "bicing",
                                        "base_url": "http://wservice.viabicing.cat/v2/stations"
                              }
                  }
            }
        }

    def get(self):
        return self.config