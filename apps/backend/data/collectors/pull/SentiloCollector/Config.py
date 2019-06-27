class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "sentilo": {
                              "source_name": "sentilo",
                              "pre_base_url": "http://preconnectaapi.bcn.cat/",
                              "base_url": "http://connectaapi.bcn.cat/",
                              "providers": ["CESVA"] , #"SMC", "SIGE_PR", "CIRCUTOR", "ARKENOVA", "ARELSA"]
                            }
            },
            "tokens": {
                  "sentilo":
                          {
                            "pre_production_token": "",
                            "production_token": "",
                            "endpoint": {
                                            "public_ipaddress": "84.88.76.35",
                                            "private_ipaddress": "127.0.0.1",
                                            "port": 80,
                                            "protocol": "http"
                            }
                          }
            }
        }

    def get(self):
        return self.config
