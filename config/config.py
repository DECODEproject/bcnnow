class Config:

    def __init__(self):
        self.config = {
            "api": {
                  "v0": {
                          "ipaddress": "http://84.88.76.35",
                          "port": 9530,
                          "database_url": ""
                  }
            },
            "collectors": {
                  "common": {
                            "destination": "mongodb"
                  }
            },
            "storage": {
                  "ipaddress": "localhost",
                  "port": 27017,
                  "dbname": "decode",
                  "clname": "bcnnow",
                  "topic": "decode-bcnnow"
            },
            "project": {
                  "base_url": "/home/code/projects/decode-bcnnow/",
            }
        }

    def get(self):
        return self.config