class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "odi": {
                              "source_name": "odi",
                              "iris": {
                                          "source_name": "iris",
                                          "base_url": "http://opendata-ajuntament.barcelona.cat/data",
                                          "api_base_url": "/api/action/datastore_search?resource_id=",
                                          "complaint_urls": [ '957aee59-503f-4760-b759-2b923f637c5b',
                                                              '3544d426-dda7-49ae-9378-13689113b065',
                                                              #'c3acbbed-3949-4d1c-8532-9f7a2c7fc638',
                                                              #'80e94972-1b4a-4162-8c7f-d4b356eb1554',
                                                              #'b92e1902-de85-43ab-b438-9e1679d00886'
                                                            ]
                                        }
                  }
            }
        }

    def get(self):
        return self.config