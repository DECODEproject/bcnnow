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

# This class defines a set of configuration variables for Smart Citizen collector.
class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                "iot": {
                    "ca9bc7f7-5689-47fa-8215-c78c104c8d3c": {
                        "community_id": "ca9bc7f7-5689-47fa-8215-c78c104c8d3c",
                        "community_seckey": "CPzY3PvJXXwl9JVWKyLhpo36xbD3729XBZV3XoTVig8=",
                        "base_url": "https://datastore.decodeproject.eu",
                        "minutes": 2,
                    },
                    "a9c6a771-0418-405c-9000-25f6b0017bf0": {
                        "community_id": "a9c6a771-0418-405c-9000-25f6b0017bf0",
                        "community_seckey": "CPzY3PvJXXwl9JVWKyLhpo36xbD3729XBZV3XoTVig8=",
                        "base_url": "https://datastore.decodeproject.eu",
                        "minutes": 2,
                    }
                }
            }
        }

    def get(self):
        return self.config
