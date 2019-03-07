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
                "description": "Sentilo Noise Levels",
                "provider": "smartcitizen",
                "start": "2017-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Noise [dbA]",
                "targetvalue": "value",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#FF1300', '#801515'],
                "cuts": [-1, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": ["eventtype"],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#801515', '#FF1300'],
                "cuts": [-1, 3, 6, 9, 12, 15, 18, 21, 24, 27],
                "parameters": "",
                "filter_field": "",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "allowed_maps": ["points-map", "map-lines"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "allowed_maps": ["points-map", "map-polygons"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "colors": ['#b0c4de','#99b3d4','#85a1ca','#738ec0','#647bb6','#5569ad','#4856a4','#3b439b','#2d3092','#1d1b89','#000080'],
                "cuts": [-1, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "colors": ['#ffffe0','#ffe6b2','#ffcb91','#ffae79','#fe906a','#f47461','#e75758','#d53c4c','#c0223b','#a70b24','#8b0000'],
                "cuts": [-1, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                "colors": ['#faebd7','#f3dbbf','#eccca7','#e4bc90','#ddac7c','#d59d68','#cc8d57','#c27d48','#b76f3c','#ac6033','#a0522d'],
                "cuts": [-1, 10.0, 20.0, 30.0, 40.0, 50.0, 75.0, 100.0, 150.0, 200.0, 250.0],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
            },
            "11": {
                "id": "11",
                "type": "time-series",
                "name": "pam_proposal",
                "description": "Decidim PAM Proposals",
                "provider": "pam_proposal",
                "start": "2016-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Votes",
                "targetvalue": "voteCount",
                "aggregator": "sum",
                "radius": 20,
                "colors": ['#ffffe0','#ffe6b2','#ffcb91','#ffae79','#fe906a','#f47461','#e75758','#d53c4c','#c0223b','#a70b24','#8b0000'],
                "cuts": [-1, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": [],
                "allowed_bar_chart_dimensions": ["category"],
                "allowed_scatter_xy_dimensions": ["voteCount", "totalCommentsCount"],
                "allowed_scatter_color_dimensions": ["category"]
            },
            "12": {
                "id": "12",
                "type": "time-series",
                "name": "pam_meeting",
                "description": "Decidim PAM Meetings",
                "provider": "pam_meeting",
                "start": "2016-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Attendees",
                "targetvalue": "attendeeCount",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#FF1300', '#801515'],
                "cuts": [-1, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0],
                "filter_field": "",
                "parameters": "title@payload.title,title@payload.title,startTime@payload.startTime,endTime@payload.endTime,address@payload.address,attachments@payload.attachments,attendeeCount@payload.attendeeCount,",
                "details": "title@payload.title,title@payload.title,startTime@payload.startTime,endTime@payload.endTime,address@payload.address,attachments@payload.attachments,attendeeCount@payload.attendeeCount,",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": ["attendeeCount"],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
             },
            "13": {
                "id": "13",
                "type": "time-series",
                "name": "dddc_proposal",
                "description": "DDDC Proposals",
                "provider": "dddc_proposal",
                "start": "2018-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Votes",
                "targetvalue": "voteCount",
                "aggregator": "sum",
                "radius": 20,
                "colors": ['#ffffe0','#ffe6b2','#ffcb91','#ffae79','#fe906a','#f47461','#e75758','#d53c4c','#c0223b','#a70b24','#8b0000'],
                "cuts": [-1, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
                "parameters": "",
                "filter_field": "",
                "details": "",
                "allowed_maps": [],
                "allowed_bar_chart_dimensions": ["category"],
                "allowed_scatter_xy_dimensions": ["voteCount", "totalCommentsCount"],
                "allowed_scatter_color_dimensions": ["category"]
            },
            "14": {
                "id": "14",
                "type": "time-series",
                "name": "dddc_meeting",
                "description": "DDDC Meetings",
                "provider": "dddc_meeting",
                "start": "2018-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "Attendees",
                "targetvalue": "attendeeCount",
                "aggregator": "avg",
                "radius": 20,
                "colors": ['#004304', '#51A759', '#FFF592', '#FFDB2B', '#F55E00', '#801515'],
                "cuts": [-1, 5.0, 10.0, 15.0, 20.0, 25.0],
                "filter_field": "",
                "parameters": "title@payload.title,title@payload.title,startTime@payload.startTime,endTime@payload.endTime,address@payload.address,attachments@payload.attachments,attendeeCount@payload.attendeeCount,",
                "details": "title@payload.title,title@payload.title,startTime@payload.startTime,endTime@payload.endTime,address@payload.address,attachments@payload.attachments,attendeeCount@payload.attendeeCount,",
                "allowed_maps": ["points-map", "heat-map"],
                "allowed_bar_chart_dimensions": [],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
             },
            "15": {
                "id": "15",
                "type": "time-series",
                "name": "dddc_survey",
                "description": "DDDC Surveys",
                "provider": "dddc_survey",
                "start": "2018-01-01T00:00:00Z",
                "end": None,
                "language": "English",
                "labels": "",
                "targetvalue": "",
                "aggregator": "",
                "radius": 20,
                "colors": ['#004304', '#51A759', '#FFF592', '#FFDB2B', '#F55E00', '#801515'],
                "cuts": [-1, 5.0, 10.0, 15.0, 20.0, 25.0],
                "filter_field": "",
                "parameters": "",
                "details": "",
                "allowed_maps": [],
                "allowed_bar_chart_dimensions": ["gender", "age", "country", "continent", "education", "workSituation", "organization", "city", "district", "device", "scale", "interest"],
                "allowed_scatter_xy_dimensions": [],
                "allowed_scatter_color_dimensions": []
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
                        "id": "widget-0",
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
                        "type" : None,
                        "map_data_type": "dynamic"
                    }
                ]
            },
            "page-1": {
                "name": "Mobility with Bikes",
                "id": 2,
                "widgets":  [
                    {
                        "id": "widget-3553",
                        "title": "Explore average number of available bikes per station in neighbourhoods",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T00:00:00Z",
                        "sources": [{
                            "id": "4",
                            "aggregation": "neighbourhood",
                            "chart": "map-points",
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2018-01-01T00:00:00Z",
                            "end": "2018-06-30T00:00:00Z",
                            "dataset": None,
                            "markers": None
                        },{
                            "id": "4",
                            "aggregation": "none",
                            "chart": "map-points",
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "static"
                    }
                    ]
            },
            "page-2": {
                "name": "Agenda with events",
                "id": 3,
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
                                "map_data_type": "points",
                                "granularity": "cumulative",
                                "keyword": "",
                                "start": "2019-01-01T00:00:00Z",
                                "end": "2020-01-01T00:00:00Z",
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
                            "type" : "map",
                            "map_data_type": "static"
                        }
                    ]
            },
            "page-3": {
                "name": "Awareness on Noise",
                "id": 4,
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "static"
                    }
                ]
            },
            "page-4": {
                "name": "Photovoltaic Potential",
                "id": 5,
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
                    }
                ]
            },
            "page-5": {
                "name": "Housing",
                "id": 6,
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
                            "map_data_type": "points",
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
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
                            "map_data_type": "points",
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
                            "map_data_type": "points",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
                    }
                ]
            },
            "page-6": {
                "name": "Digital Democracy and Data Commons",
                "id": 7,
                "widgets": [
                    {
                        "id": "widget-360",
                        "title": "Meetings for the Municipal Action Plan",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "12",
                            "aggregation": "none",
                            "chart": "map-points",
                            "map_data_type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2019-01-01T00:00:00Z",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
                    },
                    {
                        "id": "widget-361",
                        "title": "Meetings for DECODE pilot",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "14",
                            "aggregation": "none",
                            "chart": "map-points",
                            "map_data_type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
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
                        "type" : "map",
                        "map_data_type": "dynamic"
                    },
                    {
                        "id": "widget-362",
                        "title": "Proposals for the Municipal Action Plan",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "11",
                            "xDim": "totalCommentsCount",
                            "yDim": "voteCount",
                            "colorDim": "category",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                            "scale": "sqrt"
                        }],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "scatter"
                    },
                    {
                        "id": "widget-363",
                        "title": "Proposals for DECODE pilot",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "13",
                            "xDim": "totalCommentsCount",
                            "yDim": "voteCount",
                            "colorDim": "category",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                            "scale": "linear"
                        }],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "scatter"
                    },
                    {
                        "id": "widget-364",
                        "title": "What is your gender?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "gender",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-365",
                        "title": "What is your age?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "age",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-366",
                        "title": "Where are you from? (country)",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "country",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-367",
                        "title": "Where are you from? (continent)",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "continent",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-368",
                        "title": "What is the highest educational level you have completed?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "education",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-369",
                        "title": "What is your job situation?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "workSituation",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-370",
                        "title": "If you belong to a group, NGO or organization that deals with issues related to online privacy, data governance and/or technological sovereignty, put here the name of your organization.",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "organization",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-371",
                        "title": "Where do you live?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "city",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-372",
                        "title": "What is your district? [for those who live in Barcelona]",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "district",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-373",
                        "title": "Which device do you mostly use to connect to the Internet?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "device",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-374",
                        "title": "In a scale from 0 to 5, where 0 is “no at all” and 5 is “very much”, how worried are you about the management of your data by internet companies?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "scale",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
                    },
                    {
                        "id": "widget-375",
                        "title": "What are the issues that worry you the most about the current ways in which data is managed?",
                        "authors": ["carmen"],
                        "modified": "2018-01-12T12:00:00Z",
                        "sources": [{
                            "id": "15",
                            "dimension": "interest",
                            "start": "2010-01-01T00:00:00Z",
                            "end": "2020-01-01T00:00:00Z",
                        }
                        ],
                        "timeinterval": None,
                        "map": None,
                        "refreshIntervalId": [],
                        "data": [],
                        "highmarker": [],
                        "highmarkericon": [],
                        "type" : "bar-chart",
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
