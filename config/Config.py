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
                 "sqllitedb": "decodebcn.sqlite"
            },
            "iotconfig": {
                "header": "{predicate:'schema:iotCommunity'}",
                "callbackurl": "http://bcnnow.decodeproject.eu/oauth/iot_login_callback",
                "schema": "decodewallet"
            },
            "project": {
                  "base_url": "/home/code/projects/bcnnow/",
            },
            "db": {
                "url": "mysql://root:Capitan2014@127.0.0.1:3306/bcnnow"
            "oauth": {
            },
                "client_username": "AzrWLH8xw1xGYoPBBt1lP4xl",
                "client_password": "V2CQt67jOXTpeV4BrDMumQOcka1HEpQmDWp72l1mnutz52j8"
            }
        }

    def get(self):
        return self.config
