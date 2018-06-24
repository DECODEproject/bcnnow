class Config:

    def __init__(self):
        self.config = {
            "collectors": {
                  "insideairbnb": {
                            "source_name": "insideairbnb",
                            "calendar_source_name": "calendar",
                            "listing_source_name": "listing",
                            "review_source_name": "review",
                            "base_url": "history/",
                            "listing_urls": ["2017-04-08-listings.csv"],
                            "calendar_urls": ["2017-04-08-calendar.csv"],
                            "review_urls": ["2017-04-08-reviews.csv"]
                  }
            }
        }

    def get(self):
        return self.config