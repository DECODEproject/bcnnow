function getDashboards() {

    var pages = {
        "page-0": {
            "name": "Create New Widget",
            "widgets": [
                {
                    "id": "widget-0",
                    "title": "Empty widget",
                    "authors": ["carmen"],
                    "modified": "2018-01-12T10:00:00Z",
                    "sources": [],
                    "timeinterval": null,
                    "map": null,
                    "refreshIntervalId": [],
                    "data": [],
                    "highmarker": [],
                    "highmarkericon": [],
                    "type" : null,
                    "map_data_type": "dynamic"
                }]

        },
        "page-1": {
            "name": "Mobility with Bikes",
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    },{
                        "id": "4",
                        "aggregation": "none",
                        "chart": "map-points",
                        "map_data_type": "points",
                        "granularity": "dynamic",
                        "keyword": "",
                        "start": "2018-06-01T00:00:00Z",
                        "end": "2018-06-02T00:00:00Z",
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                            "dataset": null,
                            "markers": null
                        }
                        ],
                        "timeinterval": null,
                        "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    },
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                        "dataset": null,
                        "markers": null
                    }
                    ],
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
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
                    "timeinterval": null,
                    "map": null,
                    "refreshIntervalId": [],
                    "data": [],
                    "highmarker": [],
                    "highmarkericon": [],
                    "type" : "bar-chart",
                }
            ]
         }
    };
	
	
	
	

    return jQuery.extend(true, {}, pages);
}
