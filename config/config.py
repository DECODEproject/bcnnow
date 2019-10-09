class Config:

    def __init__(self):
        self.config = {
            "api": {
                  "v0": {
                          "ipaddress": "http://localhost",
                          "port": 8080,
                          "database_url": ""
                  }
            },
            "collectors": {
                  "common": {
                            "destination": "mongodb",
                            "collection": "collector_config"

                  }
            },
            "storage": {
                  "ipaddress": "127.0.0.1",
                  "port": 27017,
                  "dbname": "decode",
                  "clname": "bcnnow",
                  "topic": "decode-bcnnow",
                 "sqllitedb": "decodebcn.sqlite"
            },
            "iotconfig": {
                "header": "{predicate:'schema:iotCommunity'}",
                "callbackurl": "http://84.88.76.45:887/oauth/iot_login_callback",
                "schema": "decodewallet",
                "bypass": "no",
                "login_url": "https://iot.decodeproject.eu/#/"
            },
            "project": {
                  "base_url": "/home/code/projects/bcnnow/",
            },
            "db": {
                "url": "mysql://root:**@mysqldb:3306/bcnnow"
            },
            "oauth": {
                "client_username": "**",
                "client_password": "**"
            },
            "encryption":{
                    "public": "***",
                    "private": "***"

            }
        }

    def get(self):
        return self.config
