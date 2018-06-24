class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "odi": {
                              "source_name": "odi",
                              "pointsinterest": {
                                        "source_name": "pointsinterest",
                                        "base_url": "http://www.bcn.cat/tercerlloc/",
                                        "poi_urls": ['pits_opendata_en.xml']
                              }
                  }
            }
        }

    def get(self):
        return self.config