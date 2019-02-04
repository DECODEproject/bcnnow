/*
    Get cookie value
*/
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function getDatasetsForUser() {
    // if logged call server for available datasets for user
    // in other case return defaults as is

    cookieValue = getCookie("session-id");
    if (cookieValue == null) {
        cookieValue = getCookie("session-token");
    }

    if (cookieValue != null) {
        // get datasets from server
        var ret = $.ajax({
            async: false,
            url: url_root + "api/v0/get_available_datasets",
            beforeSend: function (xhr) {
                // authenticate the call 
                xhr.setRequestHeader ("Authorization", "Bearer " + cookieValue);
            },
            success: function(data) {
                // var returnValue = jQuery.extend(true, {}, data);
                return data;
            },
            error: function() {
            }
        });

        if (ret['status'] == 200) {

            responseText = ret['responseText'];
            responseJson = JSON.parse(responseText);
            return responseJson;
        }
    }

    return getDatasets();
}

function getDatasets() {

    var datasets = {
        "1": {
        "id": "1",
        "type": "time-series",
        "name": "smartcitizen",
        "description": "SmartCitizen Noise Levels",
        "provider": "smartcitizen",
        "start": "2017-01-01T00:00:00Z",
        "end": null,
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
        "labels": null,
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
        "labels": null,
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
        "end": null,
        "language": "English",
        "labels": "Available bikes [unit]",
        "targetvalue": "bikes",
        "aggregator": "sum",
        "radius": 13,
        "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#801515', '#FF1300'],
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
        "labels": null,
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
        "labels": null,
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
        "colors": ['#b0c4de','#99b3d4','#85a1ca','#738ec0','#647bb6','#5569ad','#4856a4','#3b439b','#2d3092','#1d1b89','#000080'],
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
        "colors": ['#ffffe0','#ffe6b2','#ffcb91','#ffae79','#fe906a','#f47461','#e75758','#d53c4c','#c0223b','#a70b24','#8b0000'],
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
        "colors": ['#faebd7','#f3dbbf','#eccca7','#e4bc90','#ddac7c','#d59d68','#cc8d57','#c27d48','#b76f3c','#ac6033','#a0522d'],
        "cuts": [-1, 10.0, 20.0, 30.0, 40.0, 50.0, 75.0, 100.0, 150.0, 200.0, 250.0],
        "parameters": "",
        "filter_field": "",
        "details": "",
        "allowed_visual_models": ["points-map", "heat-map"]
        }
    };

    return jQuery.extend(true, {}, datasets);
}