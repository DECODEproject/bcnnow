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
                            "pre_production_token": "3e82f3d12f4c6ed75248e51d31c4eec05caaa9f2e63a2022043127fdc829d4a8",
                            "production_token": "53870377a55ba12a824f98577fa89aa0d967972375ec8be9992646478b8a835a",
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
