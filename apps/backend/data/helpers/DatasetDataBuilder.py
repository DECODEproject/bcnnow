from pymongo import MongoClient
import datetime
from config.Config import Config as globalConfig

globalCfg = globalConfig().get()


class DataSetDataBuilder:

    def __init__(self, ):
        return

    # Start reader process
    def start(self):
        print(str(datetime.datetime.now()) + ' ' + 'Start saving dataset')
        data = self.get_data()
        self.save_data(data)
        print(str(datetime.datetime.now()) + ' ' + 'End saving dataset')

    @staticmethod
    def store(data):
        client = MongoClient(globalCfg['storage']['ipaddress'], globalCfg['storage']['port'])
        db = client[globalCfg['storage']['dbname']]
        collection = db["datasets"]

        try:
            if collection.find({"id": data['id']}).count() == 0:
                collection.insert_one(data)
            else:
                collection.update_one({"id": data['id']}, {"$set": data}, upsert=False)
        except:
            print(str(datetime.datetime.now()) + ' ' + 'Error')

    @staticmethod
    def get_data():
        return {
            "1": {
                "id": "1",
                "type": "time-series",
                "name": "smartcitizen",
                "description": "SmartCitizen Noise Levels",
                "provider": "smartcitizen",
                "start": "2017-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Noise [dbA]",
                "targetvalue": "value",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E',
                           '#F55E00', '#FF1300', '#801515'],
                "cuts": [-1, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "2": {
                "id": "2",
                "type": "record",
                "name": "asia",
                "description": "ASIA Events",
                "provider": "asia",
                "start": "2017-11-01T00:00:00Z",
                "end": "2018-02-01T00:00:00Z",
                "language": "Spanish",
                "labels": None,
                "targetvalue": 1,
                "aggregator": "count",
                "radius": 20,
                "colors": ['#01579B'],
                "cuts": [-1],
                "parameters": "name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,",
                "details": 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,',
                "filter_field": "payload.name",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "3": {
                "id": "3",
                "type": "record",
                "name": "iris",
                "description": "IRIS Claims",
                "provider": "iris",
                "start": "2014-01-01T00:00:00Z",
                "end": "2018-01-01T00:00:00Z",
                "language": "Catalan",
                "labels": None,
                "aggregator": "count",
                "targetvalue": 1,
                "radius": 10,
                "colors": ['#E91E63'],
                "cuts": [-1],
                "parameters": "element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,",
                "details": 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,',
                "filter_field": "payload.element",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "4": {
                "id": "4",
                "type": "time-series",
                "name": "bicing",
                "description": "ODI Bicing Stations",
                "provider": "odi",
                "start": "2017-11-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Available bikes [unit]",
                "targetvalue": "bikes",
                "aggregator": "sum",
                "radius": 13,
                "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E',
                           '#F55E00', '#801515', '#FF1300'],
                "cuts": [-1, 3, 6, 9, 12, 15, 18, 21, 24, 27],
                "parameters": "",
                "filter_field": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "5": {
                "id": "5",
                "type": "record",
                "name": "insideairbnb",
                "description": "Airbnb Listings",
                "provider": "insideairbnb",
                "start": "2017-04-08T00:00:00Z",
                "end": "2017-04-08T00:00:00Z",
                "language": "English",
                "labels": None,
                "targetvalue": 1,
                "aggregator": "count",
                "radius": 3,
                "colors": ['#004304'],
                "cuts": [-1],
                "parameters": "",
                "filter_field": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "6": {
                "id": "6",
                "type": "record",
                "name": "cityos-ptt_carril_bici",
                "description": "CityOS Bike Lanes",
                "provider": "cityos-ptt_carril_bici",
                "start": "2018-04-01T00:00:00Z",
                "end": "2018-05-01T00:00:00Z",
                "language": "Catalan",
                "labels": None,
                "targetvalue": 1,
                "aggregator": "count",
                "radius": 20,
                "colors": ['#003366'],
                "cuts": [-1],
                "parameters": "line@payload.line,",
                "filter_field": "",
                "allowed_visual_models": ["points-map", "map-lines"]
            },
            "7": {
                "id": "7",
                "type": "record",
                "name": "cityos-potencial_fotovoltaic",
                "description": "CityOS Photovoltaic Potencial",
                "provider": "cityos-potencial_fotovoltaic",
                "start": "2018-06-13T00:00:00Z",
                "end": "2018-06-14T00:00:00Z",
                "language": "English",
                "labels": "Potential [unit]",
                "targetvalue": "powth",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#004304', '#86C98A', '#FFF592', '#FFDB2B', '#F55E00', '#FF1300', '#801515'],
                "cuts": [-1, 500, 550, 600, 650, 700, 750],
                "parameters": "polygon@payload.polygon,",
                "filter_field": "",
                "allowed_visual_models": ["points-map", "map-polygons"]
            },
            "8": {
                "id": "8",
                "type": "time-series",
                "name": "ohb",
                "description": "Touristic House Offer",
                "provider": "ohb",
                "start": "2017-01-01T00:00:00Z",
                "end": "2017-03-01T00:00:00Z",
                "language": "English",
                "labels": "# per 1000 inhabitants",
                "targetvalue": "value",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#b0c4de', '#99b3d4', '#85a1ca', '#738ec0', '#647bb6', '#5569ad', '#4856a4', '#3b439b',
                           '#2d3092', '#1d1b89', '#000080'],
                "cuts": [-1, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "9": {
                "id": "9",
                "type": "time-series",
                "name": "ohb2",
                "description": "Monthly Rent Price",
                "provider": "ohb2",
                "start": "2005-01-01T00:00:00Z",
                "end": "2016-01-01T00:00:00Z",
                "language": "English",
                "labels": "€ m2/month",
                "targetvalue": "value",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#ffffe0', '#ffe6b2', '#ffcb91', '#ffae79', '#fe906a', '#f47461', '#e75758', '#d53c4c',
                           '#c0223b', '#a70b24', '#8b0000'],
                "cuts": [-1, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            },
            "10": {
                "id": "10",
                "type": "time-series",
                "name": "ohb3",
                "description": "Hotels",
                "provider": "ohb3",
                "start": "2017-01-01T00:00:00Z",
                "end": "2017-03-01T00:00:00Z",
                "language": "English",
                "labels": "# per 1000 inhabitants",
                "targetvalue": "value",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#faebd7', '#f3dbbf', '#eccca7', '#e4bc90', '#ddac7c', '#d59d68', '#cc8d57', '#c27d48',
                           '#b76f3c', '#ac6033', '#a0522d'],
                "cuts": [-1, 10.0, 20.0, 30.0, 40.0, 50.0, 75.0, 100.0, 150.0, 200.0, 250.0],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_visual_models": ["points-map", "heat-map"]
            }
        }

    # Save data to permanent storage
    def save_data(self, data):
        for item in data.items():
            self.store(item[1])


class DashboardsDataBuilder:

    def __init__(self, ):
        return

    # Start reader process
    def start(self):
        print(str(datetime.datetime.now()) + ' ' + 'Start saving dashboard')
        data = self.get_data()
        self.save_data(data)
        print(str(datetime.datetime.now()) + ' ' + 'End saving dashboard')

    @staticmethod
    def store(data):
        client = MongoClient(globalCfg['storage']['ipaddress'], globalCfg['storage']['port'])
        db = client[globalCfg['storage']['dbname']]
        collection = db["dashboards"]

        try:
            if collection.find({"id": data[1]["id"]}).count() == 0:
                collection.insert_one(data[1])
            else:
                collection.update_one({"id": data[1]['id']}, {"$set": data[1]}, upsert=False)
        except:
            print(str(datetime.datetime.now()) + ' ' + 'Error')

    @staticmethod
    def get_data():
        return {
            "page-0": {
                "id": 1,
                "name": "Create New Widget",
                "widgets": [
                    {
                        "id": "widget-45453",
                        "title": "Empty widget",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T10:00:00Z",
                        "sources": [],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    }]

            },
            "page-1": {
                "id": 2,
                "name": "Mobility with Bikes",
                "widgets": [
                    {
                        "id": "widget-3553",
                        "title": "Explore average number of available bikes per station in neighbourhoods",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T00:00:00Z",
                        "active": True,
                        "sources": [{
                            "id": "4",
                            "aggregation": "neighbourhood",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "dynamic",
                            "keyword": "",
                            "start": "2018-06-12T00:00:00Z",
                            "end": "2018-06-13T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-fdf",
                        "title": "Combine bike sharing usage and bike lane distribution",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T20:00:00Z",
                        "sources": [{
                            "id": "6",
                            "aggregation": "none",
                            "chart": "map-lines",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2018-01-01T00:00:00Z",
                            "end": "2018-06-30T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }, {
                            "id": "4",
                            "aggregation": "none",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "dynamic",
                            "keyword": "",
                            "start": "2018-06-01T00:00:00Z",
                            "end": "2018-06-02T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "static"
                    }
                ]
            },
            "page-2": {
                "id": 3,
                "name": "Agenda with events",
                "widgets": [
                    {
                        "id": "widget-5467",
                        "title": "Find City Events Around You",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T20:00:00Z",
                        "sources": [{
                            "id": "2",
                            "aggregation": "none",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2018-05-01T00:00:00Z",
                            "end": "2018-05-02T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "static"
                    }
                ]
            },
            "page-3": {
                "id": 4,
                "name": "Awareness on Noise",
                "widgets": [
                    {
                        "id": "widget-343",
                        "title": "Explore temporal noise patterns",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "1",
                            "aggregation": "none",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "dynamic",
                            "keyword": "",
                            "start": "2018-06-11T00:00:00Z",
                            "end": "2018-06-12T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-657",
                        "title": "Explore temporal average noise levels by neighbourhood",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "1",
                            "aggregation": "neighbourhood",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "dynamic",
                            "keyword": "",
                            "start": "2018-06-12T00:00:00Z",
                            "end": "2018-06-13T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-3553",
                        "title": "Distribution of claims regarding noise",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T13:00:00Z",
                        "sources": [{
                            "id": "3",
                            "aggregation": "none",
                            "chart": "heat-map",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "soroll",
                            "start": "2017-06-01T00:00:00Z",
                            "end": "2018-05-21T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        },
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "static"
                    }
                ]
            },
            "page-4": {
                "id": 5,
                "name": "Photovoltaic Potential",
                "widgets": [
                    {
                        "id": "widget-fdfd",
                        "title": "Explore photovoltaic potential distribution",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "7",
                            "aggregation": "none",
                            "chart": "map-polygons",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2018-06-11T00:00:00Z",
                            "end": "2018-06-15T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    }
                ]
            },
            "page-5": {
                "id": 6,
                "name": "Housing",
                "widgets": [
                    {
                        "id": "widget-879",
                        "title": "Explore touristic housing usage per 1,000 inhabitants together with Airbnb offer",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "8",
                            "aggregation": "district",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2016-06-11T00:00:00Z",
                            "end": "2018-06-12T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        },
                            {
                                "id": "5",
                                "aggregation": "none",
                                "chart": "heat-map",
                                "type": "points",
                                "granularity": "cumulative",
                                "keyword": "",
                                "start": "2016-06-11T00:00:00Z",
                                "end": "2018-06-12T00:00:00Z",
                                "dataset": None,
                                "markers": None
                            }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-0683",
                        "title": "Explore average contract rental income per m2 over years",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "9",
                            "aggregation": "district",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "dynamic",
                            "keyword": "",
                            "start": "2004-06-11T00:00:00Z",
                            "end": "2018-06-12T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-0295",
                        "title": "Explore room offer in hotels per 1,000 inhabitants",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "10",
                            "aggregation": "district",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2010-06-11T00:00:00Z",
                            "end": "2018-06-12T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    },
                    {
                        "id": "widget-5363",
                        "title": "Explore room offer in hotels per 1,000 inhabitants together with Airbnb offer",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "10",
                            "aggregation": "district",
                            "chart": "map-points",
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2010-06-11T00:00:00Z",
                            "end": "2018-06-12T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        },
                            {
                                "id": "5",
                                "aggregation": "none",
                                "chart": "heat-map",
                                "type": "points",
                                "granularity": "cumulative",
                                "keyword": "",
                                "start": "2016-06-11T00:00:00Z",
                                "end": "2018-06-12T00:00:00Z",
                                "dataset": None,
                                "markers": None
                            }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type": "dynamic"
                    }
                ]
            }
        }

    # Save data to permanent storage
    def save_data(self, data):
        for item in data.items():
            self.store(item)


if __name__ == "__main__":
    DataSetDataBuilder().start()
    DashboardsDataBuilder().start()
