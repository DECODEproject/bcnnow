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