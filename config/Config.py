class Config:

    def __init__(self):
        self.config = {
            "api": {
                  "v0": {
                          "ipaddress": "http://localhost",
                          "port": 9530,
                          "database_url": ""
                  }
            },
            "collectors": {
                  "common": {
                            "destination": "mongodb",
                            "collection":"collector_config"

                  }
            },
            "storage": {
                  "ipaddress": "localhost",
                  "port": 27017,
                  "dbname": "decode",
                  "clname": "bcnnow",
                  "topic": "decode-bcnnow",
                 "sqllitedb": "decodebcn"
            },
            "iotconfig": {
                "header": "{predicate:'schema:iotCommunity'}",
                "callbackurl": "decodeurl"
            },
            "project": {
                  "base_url": "/home/rohit.kumar/Documents/Projects/Decode/code/bcnnow/",
            }
        }

    def get(self):
        return self.config