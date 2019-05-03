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
                  "ipaddress": "mongodb",
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
                "url": "mysql://root:Capitan2014@mysqldb:3306/bcnnow"
            },
            "oauth": {
                "client_username": "AzrWLH8xw1xGYoPBBt1lP4xl",
                "client_password": "V2CQt67jOXTpeV4BrDMumQOcka1HEpQmDWp72l1mnutz52j8"
            },
            "encryption":{
                    "public": "BE5k24WolPVFB0OLjYZk0/VMSewVr4MARy8YfU8vGEaNIJDVqK3BUd/NVi7wctITK2+3AnwWNFwCV/oPsvhdBek=",
                    "private": "CPzY3PvJXXwl9JVWKyLhpo36xbD3729XBZV3XoTVig8="

            }
        }

    def get(self):
        return self.config
