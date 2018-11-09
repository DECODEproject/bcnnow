function getDashboards() {

    var pages = {
        "page-0": {
            "name": "Create New Widget",
            "widgets": [
                {
                    "id": "widget-45453",
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
                    "type": "dynamic"
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
                        "type": "points",
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
                        "dataset": null,
                        "markers": null
                    },{
                        "id": "4",
                        "aggregation": "none",
                        "chart": "map-points",
                        "type": "points",
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
                    "type": "static"
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
                            "type": "points",
                            "granularity": "cumulative",
                            "keyword": "",
                            "start": "2018-05-01T00:00:00Z",
                            "end": "2018-05-02T00:00:00Z",
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
                        "type": "static"
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
                        "type": "points",
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
                    "type": "static"
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
                        "type": "points",
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
                    "type": "dynamic"
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
                        "type": "points",
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
                        "type": "points",
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
                        "dataset": null,
                        "markers": null
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
                    "type": "dynamic"
                }
            ]
        },
        "page-6": {
            "name": "Decidim (beta)",
            "widgets": [
                {
                    "id": "widget-363",
                    "title": "Proposals for the Municipal Action Plan",
                    "authors": ["carmen"],
                    "modified": "2018-01-12T12:00:00Z",
                    "sources": [{
                        "id": "11",
                        "aggregation": "district",
                        "chart": "map-points",
                        "type": "points",
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
                    "type": "dynamic"
                },
                {
                    "id": "widget-2125",
                    "title": "Meetings for the Municipal Action Plan",
                    "authors": ["carmen"],
                    "modified": "2018-01-12T12:00:00Z",
                    "sources": [{
                        "id": "12",
                        "aggregation": "none",
                        "chart": "map-points",
                        "type": "points",
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
                    "type": "dynamic"
                }
            ]
         }
    };
	
	
	
	

    return jQuery.extend(true, {}, pages);
}
