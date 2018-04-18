
    var doubleClickTime = 0;
    var threshold = 200;
    var lineColors = ['#4D9DE0', '#E15554', '#E1BC29', '#3BB273', '#7768AE'];

    function shareDashboard() {
        $('#popup-dashboard').click(function(e){
            var page_id = page;
            var shared_widgets = {'widgets': []};
            pages[page_id]['widgets'].forEach(function(widget, windex){
                shared_widget = widget;
                shared_widget['sources'].forEach(function(source, sindex){
                    widget['map'] = null;
                    widget['sources'][sindex]['markers'] = null;
                    widget['sources'][sindex]['dataset'] = null;
                    widget['timeinterval'] = null;
                });
                shared_widgets.widgets.push(shared_widget);
            });
            makeShort('Copy this link to share your dashboard', window.location.href + '?widgets=' + JSON.stringify(shared_widgets));
        });
    }

    function shareWidget(element) {
        var widget_id = pages[page]['widgets'][$(element).attr('id').split('-')[0]]['id'];
        var page_id = page;
        var shared_widget = {};
        pages[page_id]['widgets'].forEach(function(widget, windex){
            if(widget['id'] == widget_id) {
                shared_widget = widget;
                shared_widget['sources'].forEach(function(source, sindex){
                    widget['sources'][sindex]['markers'] = null;
                    widget['sources'][sindex]['dataset'] = null;
                    widget['map'] = null;
                    widget['timeinterval'] = null;
                    widget['highmarkericon'] = [];
                    widget['refreshIntervalId'] = null;
                    widget['highmarker'] = [];
                    widget['data'] = [];
                });
            }
        });

        makeShort('Copy this link to share your widget', window.location.href + '?widget=' + JSON.stringify(shared_widget));
    }

    function makeShort(text, link, show=true){
        gapi.client.setApiKey('AIzaSyBnD5ih866EjgWgzL01iTjngGMWaSdFhiw');
        gapi.client.load('urlshortener', 'v1', function(){
            var request = gapi.client.urlshortener.url.insert({
                'resource': {
                    'longUrl': link
                }
            });
            request.execute(function(response)  {
                if(show) {
                    try {
                        BootstrapDialog.alert({
                            title: text,
                            message: '<a href="' + response.id + '" target="_blank">' + response.id + '</a>'
                        });
                    }
                    catch(err) {
                    }
                }
            });
        });
    }

    function allowDrop(ev) {


        ev.preventDefault();
    }

    function drag(ev) {
        ev.dataTransfer.setData("text", ev.target.id);
    }

    function drop(ev) {
        ev.preventDefault();
        var widget_id = pages[page]['widgets'][ev.dataTransfer.getData("text").split('-')[0]]['id'];
        var target_page_id = ev.target.id;
        var previous_page_id = page;
        var moved_widget = {};
        var index = -1;
        if(target_page_id != '') {
            $('#' + widget_id).remove();
            pages[previous_page_id]['widgets'].forEach(function(widget, windex){
                if(widget['id'] == widget_id) {
                    moved_widget = widget;
                    index = windex;
                }
            });
            pages[previous_page_id]['widgets'].splice(index, 1);
            pages[target_page_id]['widgets'].push(moved_widget);
            $.notify('You have moved your widget "' + moved_widget['title'] + '" on the dashboard page "' + pages[target_page_id]['name'] + '".', "success");
        }
    }

    function getType(sources) {
        var value = 'static';
        sources.forEach(function(source, index){
            if(source['granularity'] != 'cumulative') {
                value = 'dynamic';
            }
        });
        return value;
    }

    var datasets = {
        "1": {
        "type": "time-series",
        "name": "smartcitizen",
        "description": "Noise levels",
        "provider": "smartcitizen",
        "start": "2017-01-01T00:00:00Z",
        "end": null,
        "language": "English",
        "labels": "Noise [dbA]",
        "targetvalue": "value",
        "aggregator": "avg",
        "radius": 20,
        "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#FF1300', '#801515'],
        "cuts": [-1, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84]
        },
        "2": {
        "type": "record",
        "name": "asia",
        "description": "City events",
        "provider": "asia",
        "start": "2017-11-01T00:00:00Z",
        "end": "2018-02-01T00:00:00Z",
        "language": "Spanish",
        "labels": null,
        "targetvalue": 1,
        "aggregator": "count",
        "radius": 20,
        "colors": ['#01579B'],
        "cuts": [-1]
        },
        "3": {
        "type": "record",
        "name": "iris",
        "description": "City claims and suggestions",
        "provider": "iris",
        "start": "2014-01-01T00:00:00Z",
        "end": "2018-01-01T00:00:00Z",
        "language": "Catalan",
        "labels": null,
        "aggregator": "count",
        "targetvalue": 1,
        "radius": 10,
        "colors": ['#E91E63'],
        "cuts": [-1]
        },
        "4": {
        "type": "time-series",
        "name": "bicing",
        "description": "Bicing bikes",
        "provider": "odi",
        "start": "2017-11-01T00:00:00Z",
        "end": null,
        "language": "English",
        "labels": "Available bikes [unit]",
        "targetvalue": "bikes",
        "aggregator": "avg",
        "radius": 10,
        "colors": ['#004304', '#116416', '#51A759', '#86C98A', '#FFF592', '#FFE256', '#FFDB2B', '#FF6A0E', '#F55E00', '#801515', '#FF1300'],
        "cuts": [-1, 3, 6, 9, 12, 15, 18, 21, 24, 27]
        },
        "5": {
        "type": "record",
        "name": "insideairbnb",
        "description": "Airbnb listings",
        "provider": "insideairbnb",
        "start": "2017-04-08T00:00:00Z",
        "end": "2017-04-08T00:00:00Z",
        "language": "English",
        "labels": null,
        "targetvalue": 1,
        "aggregator": "count",
        "radius": 3,
        "colors": ['#004304'],
        "cuts": [-1]
        }
    };


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
            "name": "Bicing Station Patterns",
            "widgets": [
                {
                    "id": "widget-3553",
                    "title": "Explore temporal bicing patterns",
                    "authors": ["carmen"],
                    "modified": "2018-01-12T00:00:00Z",
                    "sources": [{
                        "id": "4",
                        "aggregation": "none",
                        "chart": "map-points",
                        "type": "points",
                        "granularity": "minutes",
                        "keyword": "",
                        "start": "2018-01-18T00:00:00Z",
                        "end": "2018-01-19T00:00:00Z",
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
        "page-2": {
            "name": "City Events Search",
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
                        "start": "2018-01-01T00:00:00Z",
                        "end": "2018-01-30T00:00:00Z",
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
            "name": "Noise Level Awareness",
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
                        "granularity": "hours",
                        "keyword": "",
                        "start": "2018-01-30T00:00:00Z",
                        "end": "2018-01-31T00:00:00Z",
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
                    "title": "Explore claims, suggestions, and incidents regarding noise",
                    "authors": ["carmen"],
                    "modified": "2018-01-12T13:00:00Z",
                    "sources": [{
                        "id": "3",
                        "aggregation": "none",
                        "chart": "heat-map",
                        "type": "points",
                        "granularity": "cumulative",
                        "keyword": "soroll",
                        "start": "2017-04-03T00:00:00Z",
                        "end": "2018-01-30T00:00:00Z",
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
        }
    };


$(document).ready(function() {
    var api_endopoint = 'http://5f14ad67.ngrok.io';
    var current_latitude = 0;
    var current_longitude = 0;
    var start_date = moment().subtract('days', 6).toISOString();
    var end_date = moment().toISOString();
    var options = { weekday: "long", year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" };
    var new_shared_widget = decodeURIComponent(window.location.href).split('widget=')[1];
    var new_shared_widgets = decodeURIComponent(window.location.href).split('widgets=')[1];

    function initialize_map(windex, sindex) {
        $("#" + pages[page]['widgets'][windex]['id'] + "-loader").show();
        pages[page]['widgets'][windex]['sources'][sindex]['markers'] = new L.LayerGroup();
        try {
            map = L.map(pages[page]['widgets'][windex]['id'] + '-map').setView([41.390205,2.154007], 12);
            L.tileLayer.grayscale('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 18,
                id: 'mapbox.streets',
                accessToken: 'pk.eyJ1IjoibW1hcnJhcyIsImEiOiJjamE3MnBpd2E3MjZ1MndwNzY5YjBrdDgxIn0.zO2nGOwmSGhb8YrzhWNdeQ'
            }).addTo(map);
        }
        catch(err) {
            map = pages[page]['widgets'][windex]['map'];
        }
        c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
        pages[page]['widgets'][windex]['map'] = map;
        var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
        var qtxt = ''
        other_par = '';
        par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
        par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
        if(c == 'iris') {
            other_par = par_iris;
            if (query != '') {
                qtxt = "&$payload.element=[" + query + "]";
            }
        }
        if(c == 'asia') {
            other_par = par_asia;
            if (query != '') {
                qtxt = "&$payload.name=[" + query + "]";
            }
        }
        var aggregation = '';
        var operators = '';
        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
            aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
            operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
        }
        console.log(api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'] + qtxt);
        $.ajax({
            url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'] + qtxt,
            success: function(data) {
                try {
                    if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
                        filtered = {"records": [], "count": 0}
                        data.records.forEach(function(record) {
                            var filtered_records = {"_id": record._id, "doc": []};
                            record.doc.forEach(function(element) {
                                var r = {};
                                var lat = 0.0;
                                var long = 0.0;
                                var num = 0
                                element.doc.forEach(function(h) {
                                    if(h["point"][1] > 1) {
                                        num += 1;
                                    }
                                    lat += h["point"][1];
                                    long += h["point"][0];
                                });
                                if(num > 0) {
                                    r["id"] = element["_id"][pages[page]['widgets'][windex]['sources'][sindex]['aggregation']];
                                    r["point"] = [long / num, lat / num];
                                    r["value"] = element["avg"];
                                    r["count"] = element["count"];
                                    r["avg"] = element["avg"];
                                    r["sum"] = element["sum"];
                                    filtered_records.doc.push(r);
                                }
                            });
                            if(filtered_records.doc.length > 0) {
                                filtered.records.push(filtered_records);
                            }
                        });
                        filtered.count = filtered.records.length;
                        data.records = filtered.records;
                        data.count = filtered.count;
                    }
                    else {
                        filtered = {"records": [], "count": 0}
                        data.records.forEach(function(record) {
                            var filtered_records = {"_id": record._id.timestamp, "doc": []};
                            record.doc.forEach(function(element) {
                                if(element.point[0] > 1) {
                                    filtered_records.doc.push(element);
                                }
                            });
                            if(filtered_records.doc.length > 0) {
                                filtered.records.push(filtered_records);
                            }
                        });
                        filtered.count = filtered.records.length;
                        data.records = filtered.records;
                        data.count = filtered.count;
                    }

                    pages[page]['widgets'][windex]['sources'][sindex]['dataset'] = data;
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider({
                        range: "min",
                        min: 1,
                        max: pages[page]['widgets'][windex]['sources'][sindex]['dataset'].count,
                        step: 1,
                        slide: function( event, ui ) {
                            update_map(windex, sindex);
                        }
                    });
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider-value").text('Click "Play" to see levels along time');
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider('value', 0);

                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['colors'].length > 1) {
                        var legend = L.control({position: 'bottomright'});
                        legend.onAdd = function (map) {
                            var div = L.DomUtil.create('div', 'info legend');
                            var faultstatus = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['cuts'];
                            div.innerHTML += '<strong> ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ' </strong> <br>';
                            for (var i = faultstatus.length-1; i >= 0; i--) {
                                div.innerHTML += '<i class="circle" style="background:' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['colors'][i] + '"></i> ' + (faultstatus[i+1] ? '' : '&ge; ') + (faultstatus[i]+1) + (faultstatus[i+1] ? ' - ' + (faultstatus[i+1]) : '') + '<br>';
                            }
                            return div;
                        };
                        legend.addTo(pages[page]['widgets'][windex]['map']);
                    }
                    update_map(windex, sindex, 0);
                    $("#" + pages[page]['widgets'][windex]['id'] + "-loader").hide();
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider-button").show();
                }
                catch(err) {
                    console.log(err);
                }
            },
            error: function() {

            }
        });
    }

    function getIcon(dataset, value) {
        var colors = dataset['colors'];
        var cuts = dataset['cuts'];
        var color = '#000000';

        cuts.forEach(function (cut, i) {
            if(cut < value) {
                color = colors[i];
            }
        });

        return L.vectorIcon({
                  className: 'circle-icon',
                  svgHeight: 32,
                  svgWidth: 32,
                  type: 'circle',
                  shape: {
                    r: '5',
                    cx: '16',
                    cy: '16'
                  },
                  style: {
                    fill: color,
                    stroke: color,
                    strokeWidth: 1
                  }
        });
    }

    function getIcon(dataset, value) {
        var colors = dataset['colors'];
        var cuts = dataset['cuts'];
        var color = '#00f';

        cuts.forEach(function (cut, i) {
            if(cut < value) {
                color = colors[i];
            }
        });

        return color;
    }

    function titleCase(str) {
       var splitStr = str.toLowerCase().split(' ');
       for (var i = 0; i < splitStr.length; i++) {
           splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
       }

       str = splitStr.join(' ');
       var splitStr = str.split('\'');
       for (var i = 0; i < splitStr.length; i++) {
           splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
       }

       return splitStr.join('\'');
    }

    function getArea(feature, dataset, obs) {
        var bordercolor = 'rgba(0,0,0,0)';
        var fillcolor = 'rgba(0,0,0,0)';
        obs.forEach(function(element) {
            if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
                fillcolor = getIcon(dataset, element.value);
                bordercolor = '#000';
            }
        });

        return {
          color: bordercolor,
          weight: 1,
          opacity: 1,
          fillColor: fillcolor,
          fillOpacity: 0.8
        }
    }

    function getLabel(feature, dataset, obs) {
        var result = null;
        obs.forEach(function(element) {
            if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
                result = element;
            }
        });
        return result;
    }

    function update_map(windex, sindex, dir=1) {
        var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value") + dir;
        var max = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "max");
        var markers_layer = new L.LayerGroup();
        pages[page]['widgets'][windex]['sources'][sindex]['markers'].clearLayers();
        $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("value", (val)%(max+1) );
        footprint = moment(pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"]).format('dddd, MMMM Do YYYY, h:mm:ss a');
        $("#" + pages[page]['widgets'][windex]['id'] + "-slider-value").html("<span  class='tip'>" + footprint + "</span>");
        if(pages[page]['widgets'][windex]['sources'][sindex]['granularity'] != "cumulative") {
            obs = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["doc"];
        }
        else {
            obs = [];
            pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records.forEach(function(record, index){
                obs = obs.concat(record["doc"]);
            });

        }
        console.log(obs);
        var heatmapdata = [];

        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != "none") {
            $.ajax({
                dataType: "json",
                url: "assets/geojson/" + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ".geojson",
                success: function(data) {
                    iris_boundary = new L.geoJson(data, {
                          style: function(feature) {
                            return getArea(feature, datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obs);
                          },
                          onEachFeature: function(feature, layer) {
                              var element = getLabel(feature, datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obs);
                              if(element) {
                                  layer.on({click: function(e){
                                        var commonid = 'Ciao';
                                        $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-8');
                                        $("#" + windex + "-slider-date-graph").show();
                                        $("#" + windex + "-graph-loader").show();
                                        var aggregation = '';
                                        var operators = '';
                                        var geo = '';
                                        var agg = '';
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
                                            aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
                                            operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
                                            geo = "&$location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + commonid
                                            agg = "avg";
                                        }
                                        else {
                                            geo = "&$payload.id=" + commonid
                                            agg = 'value';
                                        }

                                        var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value");
                                        var current = '';
                                        if (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none' && (datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris')) {
                                            var val = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z';
                                            var val0 = moment(val).set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                                            var val1 = moment(val).add(1, "days").set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                                            current = "&$timestamp=gte@" + val0 + ",lt@" + val1;
                                        }
                                        else {
                                            current = "&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'];
                                        }

                                        c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
                                        var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
                                        var qtxt = ''
                                        other_par = '';
                                        par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
                                        par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
                                        if(c == 'iris') {
                                            other_par = par_iris;
                                            if (query != '') {
                                                qtxt = "&$payload.element=[" + query + "]";
                                            }
                                        }
                                        if(c == 'asia') {
                                            other_par = par_asia;
                                            if (query != '') {
                                                qtxt = "&$payload.name=[" + query + "]";
                                            }
                                        }

                                        $.ajax({
                                            url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation" + geo + current + qtxt,
                                            success: function(output) {
                                                try {
                                                    $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").empty();
                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia') {
                                                        $("#" + windex + "-time-series-title").text("ASIA ID " + commonid);
                                                        $.each(output.records, function(index, element) {
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                                 var categories = '';
                                                                 for(var k in element.doc[0].categories) categories += element.doc[0].categories[k] + '; ';
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Categories:</span> ' + categories + '</div>');
                                                            }
                                                            else {
                                                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of events:</span> ' + element.doc[0].count + '</div>');
                                                            }
                                                        });
                                                    }


                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris') {
                                                        $("#" + windex + "-time-series-title").text("IRIS ID " + commonid);
                                                        $.each(output.records, function(index, element) {
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Area:</span> ' + element.doc[0].area + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Element:</span> ' + element.doc[0].element + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Detail:</span> ' + element.doc[0].detail + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Support:</span> ' + element.doc[0].support + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Channel:</span> ' + element.doc[0].channel + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Opening Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Closing Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                            }
                                                            else {
                                                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of iris:</span> ' + element.doc[0].count + '</div>');
                                                            }
                                                        });
                                                    }

                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'smartcitizen' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'bicing') {
                                                        var sensordata = [];
                                                        var x = [];
                                                        var y = [];
                                                        $.each(output.records, function(index, element) {
                                                            var timestamp;
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {timestamp = element["_id"]}
                                                            else {timestamp = element["_id"]["timestamp"]}
                                                            x.push(timestamp);
                                                            y.push(Math.floor(element["doc"][0][agg]));
                                                        });
                                                     }
                                                    $("#" + windex + "-graph-loader").hide();
                                                }
                                                catch(err) {
                                                    console.log(err);
                                                }
                                            },
                                            error: function() {
                                            }
                                        });
                                  }});
                                  layer.bindTooltip(feature.properties.neighbourhood + ' ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ': ' + element.value);
                              }
                          }
                    });
                    pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(iris_boundary);
                    pages[page]['widgets'][windex]['map'].addLayer(pages[page]['widgets'][windex]['sources'][sindex]['markers']);
                },
                error: function() {

                }
            });
        }
        else {
            obs.forEach(function(element) {
                var value = (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none')? (typeof datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] === "string"? element[datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue']]:datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue']) : element[datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['aggregator']];
                heatmapdata.push({lat: element["point"][1], lng: element["point"][0], value: value});
                id = element["id"];
                obsval = parseInt(element["value"]);
                icon = L.vectorIcon({
                          className: 'circle-icon-' + id,
                          svgHeight: 12,
                          svgWidth: 12,
                          type: 'circle',
                          shape: {
                            r: '5',
                            cx: '6',
                            cy: '6'
                          },
                          style: {
                            fill: getIcon(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obsval),
                            stroke: '#000',
                            strokeWidth: 1
                          }
                });

                var aggregation = '';
                if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != "none") {
                    aggregation = "&location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + id;
                }

                var marker = L.marker([element["point"][1],element["point"][0]], {icon: icon, title: 'Sensor ' + id + ': ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ' ' + obsval, sentiloid: id});

                marker.on('click', function(e){
                    var commonid = e.target.options.sentiloid;
                    console.log(pages[page]);
                    pages[page]['widgets'][windex]["highmarker"].push(e.target);
                    pages[page]['widgets'][windex]["highmarkericon"].push(e.target.options.icon);
                    $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + commonid).empty();
                    e.target.setIcon(L.vectorIcon({
                      className: 'circle-icon-' + windex + '-' + sindex + '-' + commonid,
                      svgHeight: 16,
                      svgWidth: 16,
                      type: 'path',
                      shape: {
                        x: '1',
                        y: '1',
                        width: '14',
                        height: '14'
                      },
                      style: {
                        fill: lineColors[pages[page]['widgets'][windex]['data'].length],
                        stroke: '#000',
                        strokeWidth: 1
                      }
                    }));
                    $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + commonid).empty();
                    e.target.setIcon(L.vectorIcon({
                      className: 'circle-icon-' + windex + '-' + sindex + '-' + commonid,
                      svgHeight: 16,
                      svgWidth: 16,
                      type: 'rect',
                      shape: {
                        x: '1',
                        y: '1',
                        width: '14',
                        height: '14'
                      },
                      style: {
                        fill: lineColors[pages[page]['widgets'][windex]['data'].length],
                        stroke: '#000',
                        strokeWidth: 1
                      }
                    }));
                    $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-8');
                    $("#" + windex + "-slider-date-graph").show();
                    $("#" + windex + "-graph-loader").show();
                    var aggregation = '';
                    var operators = '';
                    var geo = '';
                    var agg = '';
                    if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
                        aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
                        operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
                        geo = "&$location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + commonid
                        agg = "avg";
                    }
                    else {
                        geo = "&$payload.id=" + commonid
                        agg = 'value';
                    }

                    var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value");
                    var current = '';
                    if (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none' && (datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris')) {
                        var val = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z';
                        var val0 = moment(val).set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                        var val1 = moment(val).add(1, "days").set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                        current = "&$timestamp=gte@" + val0 + ",lt@" + val1;
                    }
                    else {
                        current = "&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'];
                    }

                    c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
                    var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
                    var qtxt = ''
                    other_par = '';
                    par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
                    par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
                    if(c == 'iris') {
                        other_par = par_iris;
                        if (query != '') {
                            qtxt = "&$payload.element=[" + query + "]";
                        }
                    }
                    if(c == 'asia') {
                        other_par = par_asia;
                        if (query != '') {
                            qtxt = "&$payload.name=[" + query + "]";
                        }
                    }

                    $.ajax({
                        url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation" + geo + current + qtxt,
                        success: function(output) {
                            try {
                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").empty();
                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia') {
                                    $("#" + windex + "-time-series-title").text("ASIA ID " + commonid);
                                    $.each(output.records, function(index, element) {
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                             var categories = '';
                                             for(var k in element.doc[0].categories) categories += element.doc[0].categories[k] + '; ';
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Categories:</span> ' + categories + '</div>');
                                        }
                                        else {
                                            $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of events:</span> ' + element.doc[0].count + '</div>');
                                        }
                                    });
                                }


                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris') {
                                    $("#" + windex + "-time-series-title").text("IRIS ID " + commonid);
                                    $.each(output.records, function(index, element) {
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Area:</span> ' + element.doc[0].area + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Element:</span> ' + element.doc[0].element + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Detail:</span> ' + element.doc[0].detail + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Support:</span> ' + element.doc[0].support + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Channel:</span> ' + element.doc[0].channel + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Opening Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Closing Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                        }
                                        else {
                                            $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of iris:</span> ' + element.doc[0].count + '</div>');
                                        }
                                    });
                                }

                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'smartcitizen' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'bicing') {
                                    var sensordata = [];
                                    var x = [];
                                    var y = [];
                                    $.each(output.records, function(index, element) {
                                        var timestamp;
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {timestamp = element["_id"]}
                                        else {timestamp = element["_id"]["timestamp"]}
                                        x.push(timestamp);
                                        y.push(Math.floor(element["doc"][0][agg]));
                                    });

                                    var d3 = Plotly.d3;

                                    var WIDTH_IN_PERCENT_OF_PARENT = 100,
                                        HEIGHT_IN_PERCENT_OF_PARENT = 100;

                                    var gd3 = d3.select('#' + pages[page]['widgets'][windex]['id'] + '-dashboard-line')
                                        .append('div')
                                        .style({
                                            width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                                            'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%'
                                        });

                                    var gd = gd3.node();

                                    pages[page]['widgets'][windex]['data'].push({name: 'Sensor ' + commonid, x: x, y: y, type: 'scatter', line: {color: lineColors[pages[page]['widgets'][windex]['data'].length], width: 1}});
                                    Plotly.newPlot(gd, pages[page]['widgets'][windex]['data'], {
                                          autosize: true,
                                          height: 300,
                                          margin: {
                                            l: 35,
                                            r: 50,
                                            b: 35,
                                            t: 15,
                                            pad: 4
                                          },
                                          showlegend: true,
                                          legend: {
                                            x: 1,
                                            y: 1
                                          }
                                    });

                                    window.onresize = function() {
                                        Plotly.Plots.resize(gd);
                                    };

                                }
                                $("#" + windex + "-graph-loader").hide();
                            }
                            catch(err) {
                                console.log(err);
                            }
                        },
                        error: function() {
                        }
                    });
                });
                markers_layer.addLayer(marker);
            });
            var testData = {
              max: 8,
              data: heatmapdata
            };
            var cfg = {
              "radius": datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['radius'],
              "maxOpacity": .5,
              "useLocalExtrema": true
            };
            var heatmapLayer = new HeatmapOverlay(cfg);
            heatmapLayer.setData(testData);
            if(pages[page]['widgets'][windex]['sources'][sindex]['chart'] == 'heat-map') {
                pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(heatmapLayer);
            }
            else {
                pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(markers_layer);
            }
            pages[page]['widgets'][windex]['map'].addLayer(pages[page]['widgets'][windex]['sources'][sindex]['markers']);
        }
    }

    function displayWidgets(widgets) {
        $(".page-content-wrap").empty();
        html= '';
        widgets.forEach(function(widget, windex){
            html =  '<!-- START SENTILO BLOCK -->' +
                    '<div class="panel panel-default" ondragstart="drag(event)" draggable="true" id="' + widget['id'] + '">' +
                        '<div class="panel-heading">' +
                            '<div class="panel-title-box">' +
                                '<h3 id="id-' + widget['id'] + '" class="widget-title">' + widget['title'] + '</h3> <span class="creator-authors"> created by ';
                                widget['authors'].forEach(function(author, sindex){
                                    html +=        '<span class="high-name">' + author  + '</span>';
                                });
                                html += ' and modified at <span id="' + windex + '-modified" class="high-name">' + widget['modified'] + '</span></span>';

            html += '<span class="' + windex + '-source-list">';
            html +=         '<div class="row">' +
                                '<div class="high-name header-column col-md-2">' + 'Data' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Source' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'From' + '</div>' +
                                '<div class="high-name header-column col-md-2">' + 'To' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Filtered by' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Aggregated by' + '</div> ' +
                                '<div class="high-name header-column col-md-1"> ' + 'Commands' +  '</div> ' +
                            '</div>';
            widget['sources'].forEach(function(source, sindex){
                html +=         '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                    '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['aggregation'] != 'none' ? source['aggregation']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                    '</div> ' +
                                '</div>';
                html +=         '<div id="' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modal fade" role="dialog">' +
                                '<div class="modal-dialog">' +
                                    '<div class="modal-content">' +
                                      '<div class="modal-header">' +
                                        '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                                        '<h4 class="modal-title">Edit "' + datasets[source['id']]['provider'] + '" data source</h4>' +
                                      '</div>' +
                                          '<div class="modal-body">' +
                                              '<div class="form-group">' +
                                              '<label for="dataset">Select dataset:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-dataset">';
                jQuery.each(datasets, function(sindex, dataset){
                      html +=                   '<option value="' + sindex + '" >' + dataset['description'] + '</option>';
                });
                html +=                       '</select>' +
                                              '<div id="' + windex + '-' + sindex + '-edit-info"></div><br/>' +
                                              '<label for="time_interval">Select time interval:</label><br/>' +
                                              '<div id="' + windex + '-' + sindex + '-edit-time-interval" class="dtrange">' +
                                                    '<span></span><b class="caret"></b>' +
                                              '</div><br/><br/><br/>' +
                                              '<label for="type">Select time granularity:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-granularity">' +
                                                '<option value="cumulative">Cumulative</option>' +
                                                '<option value="minutes">Minutes</option>' +
                                                '<option value="hours">Hours</option>' +
                                                '<option value="days">Days</option>' +
                                                '<option value="weeks">Weeks</option>' +
                                                '<option value="months">Months</option>' +
                                              '</select><br/>' +
                                              '<label for="type">Select visualization type:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-type">' +
                                                '<option value="points-map" ' + (source['chart'] == 'points-map'?'selected':'') + '>Markers map</option>' +
                                                '<option value="heat-map" ' + (source['chart'] == 'heat-map'?'selected':'') + '>Heat map</option>' +
                                              '</select><br/>' +
                                              '<label for="aggregation"> Select geographical aggregation:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-aggregation">' +
                                                '<option value="none" ' + (source['aggregation'] == 'none'?'selected':'') + '>None</option>' +
                                                '<option value="neighbourhood" ' + (source['aggregation'] == 'neighbourhood'?'selected':'') + '>Neighbourhood</option>' +
                                                '<option value="district" ' + (source['aggregation'] == 'district'?'selected':'') + '>District</option>' +
                                              '</select><br/>' +
                                              '<label for="keyword">Filter by keyword:</label><br/>' +
                                              '<input class="edit-keyword" type="text" id="' + windex + '-' + sindex + '-edit-keyword" value="' + source['keyword'] + '">' +
                                              '</div>' +
                                          '</div>' +
                                      '<div class="modal-footer">' +
                                        '<button id="' + windex + '-' + sindex + '-edit-close" type="button" class="edit-close btn btn-default" data-dismiss="modal">Edit</button>' +
                                        '<button class="btn btn-default" data-dismiss="modal">Close</button>' +
                                            '</div>' +
                                    '</div>' +
                                  '</div>' +
                                '</div>';
            });

            html +=         '</span></div>' +
                            '<ul class="panel-controls panel-controls-title">' +
                               '<li class="rounded"><span id="' + windex + '-add-source" class="add-source fa fa-plus" title="Add a source"></span>' +

                               '<div id="' + windex + '-modal" class="modal fade" role="dialog">' +
                                    '<div class="modal-dialog">' +
                                        '<div class="modal-content">' +
                                          '<div class="modal-header">' +
                                            '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                                            '<h4 class="modal-title">Insert new data source</h4>' +
                                          '</div>' +
                                              '<div class="modal-body">' +
                                                  '<div class="form-group">' +
                                                  '<label for="dataset">Select dataset:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-dataset">' +
                                                    '<option value="none">None</option>';
            jQuery.each(datasets, function(sindex, dataset){
                  html +=                           '<option value="' + sindex + '">' + dataset['description'] + '</option>';
            });
            html +=                              '</select>' +
                                                 '<div id="' + windex + '-plus-info"></div><br/>' +
                                                  '<label for="time_interval">Select time interval:</label><br/>' +
                                                  '<div id="' + windex + '-plus-time-interval" class="dtrange">' +
                                                        '<span></span><b class="caret"></b>' +
                                                  '</div><br/><br/><br/>' +
                                                  '<label for="type">Select time granularity:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-granularity">' +
                                                    '<option value="cumulative">Cumulative</option>' +
                                                    '<option value="minutes">Minutes</option>' +
                                                    '<option value="hours">Hours</option>' +
                                                    '<option value="days">Days</option>' +
                                                    '<option value="weeks">Weeks</option>' +
                                                    '<option value="months">Months</option>' +
                                                  '</select><br/>' +
                                                  '<label for="type">Select visualization type:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-type">' +
                                                    '<option value="points-map">Markers map</option>' +
                                                    '<option value="heat-map">Heat map</option>' +
                                                  '</select><br/>' +
                                                  '<label for="aggregation">Select geographical aggregation:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-aggregation">' +
                                                    '<option value="none">None</option>' +
                                                    '<option value="lneighbourhood">Neighbourhood</option>' +
                                                    '<option value="district">District</option>' +
                                                  '</select><br/>' +
                                                  '<label for="keyword">Filter by keyword:</label><br/>' +
                                                  '<input type="text" id="' + windex +'-plus-keyword" text="" class="plus-keyword">' +
                                                  '</div>' +
                                              '</div>' +
                                          '<div class="modal-footer">' +
                                            '<button id="' + windex + '-btn-new-data-source" type="button" class="btn btn-default new-data-source">Insert</button>' +
                                            '<button class="btn btn-default" data-dismiss="modal">Close</button>' +
                                      '</div>' +
                                      '</div>' +
                                    '</div>' +
                                 '</li>' +
                                '<li class="' + widget['id'] + '"><a id="' + windex + '-panel-share" href="#" class="panel-share rounded"><span title="Share this widget" class="fa fa-link popup"><span class="popuptext" id="' + widget['id'] + '-popup">Popup text...</span></span></a></li>' +
                                '<li><a href="#" class="rounded move-page"><span id="' + windex + '-lizard" class="fa fa-arrows" ondragstart="drag(event)" draggable="true" title="Move this widget on the title of the dashboard where you would insert it."></span></a></li>' +
                                '<li><a href="#" class="panel-fullscreen rounded"><span title="Expand this widget" class="fa fa-expand"></span></a></li>' +
                                '<li><a href="#" id="' + windex + '-remove-page" class="rounded remove-page"><span title="Remove this widget" class="fa fa-remove remove-widget"></span></a></li>' +
                            '</ul>' +
                        '</div>' +
                        '<div class="panel-body">' +
                            '<div id="' + widget['id'] + '-loader" class="loader-container">' +
                                '<img src="img/loader.gif" width="50" height="50" class="loader">' +
                            '</div>' +
                            '<div id="' + widget['id'] + '-container" class="row stacked">' +
                                '<div id="' + windex + '-slider-date" class="col-md-12">' +
                                    '<div id="' + widget['id'] + '-map" style="height: 330px;"></div>' +
                                    '<div ' + (getType(pages[page]['widgets'][windex]['sources']) == 'static'? 'hidden': '') + ' class="row slider-date">' +
                                        '<div class="row">' +
                                            '<div id="' + widget['id'] + '-slider"></div>' +
                                        '</div>' +
                                        '<div class="col-md-12">' +
                                            '<div class="row">' +
                                                '<div class="col-md-3">' +
                                                    '<span class="slider-date button-play"><span id="' + widget['id'] + '-slider-button" class="slider-button fa fa-play"></span></span>' +
                                                    '<span class="slider-date button-back"><span id="' + widget['id'] + '-slider-button-back" class="slider-button-backward fa fa-step-backward"></span></span>' +
                                                    '<span class="slider-date button-step"><span id="' + widget['id'] + '-slider-button-step" class="slider-button-step fa fa-step-forward"></span></span>' +
                                                '</div>' +
                                                '<div class="col-md-9 slider-value">' +
                                                    '<span id="' + widget['id'] + '-slider-value"></span>' +
                                                '</div>' +
                                            '</div>' +
                                        '</div>' +
                                        '<div class="col-md-6">' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                                '<div id="' + windex + '-slider-date-graph" class="col-md-4 slider-date-graph" style="display: none;">' +
                                    '<div class="row">' +
                                        '<div class="col-md-10">' +
                                            '<div id="' + windex + '-time-series-title" class="time-series-title"></div>' +
                                        '</div>' +
                                        '<div class="col-md-2" style="text-align: right;">' +
                                            '<a id="' + windex + '-sub-widget" href="#" class="widget-control-right sub-widget-remove" data-toggle="tooltip" data-placement="top" title="" data-original-title="Remove Widget"><span class="fa fa-times"></span></a>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="row">' +
                                        '<div id="' + windex + '-graph-loader" class="loader-container">' +
                                            '<img src="img/loader.gif" width="50" height="50" class="loader">' +
                                        '</div>' +
                                        '<div class="chart-holder" id="' + widget['id'] + '-dashboard-line" width="421" height="342"></div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                    '<!-- END SENTILO BLOCK -->';

            $(".page-content-wrap").append(html);

            $('#' + widget['id'] + ' #' + windex + '-plus-dataset').on('change', function () {
                var sindex = $(this).val();
                $('#' + widget['id'] + ' #' + windex + '-plus-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[sindex]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[sindex]['end']==null? 'now': moment(datasets[sindex]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                    '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[sindex]['language'] + '</span>. </div>');
            });

            $('#' + widget['id'] + ' #' + windex + '-panel-share').click(function(){
                shareWidget(this);
            });

             $("#" + windex + "-plus-time-interval").daterangepicker({
                    ranges: {
                       'Today': [moment(), moment()],
                       'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                       'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                       'This Month': [moment().startOf('month'), moment().endOf('month')],
                       'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                    },
                    opens: 'left',
                    buttonClasses: ['btn btn-default'],
                    applyClass: 'btn-small btn-primary',
                    cancelClass: 'btn-small',
                    format: 'DD.MM.YYYY',
                    separator: ' to ',
                    startDate: moment().subtract('days', 6),
                    endDate: moment()
                  },function(start, end) {
                    start_date = start.toISOString();
                    end_date = end.toISOString();
                    $("#" + windex + "-plus-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                });
                $("#" + windex + "-plus-time-interval span").html(moment().subtract('days', 6).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

            $(".add-source").click(function(){
                var windex = $(this).attr('id').split('-')[0];
                $("#" + windex + "-modal").modal({
                    backdrop: 'static',
                    keyboard: false
                }).show();
            });

            $('.remove').click(function(e) {
                var windex = $(this).attr('id').split('-')[1];
                var sindex = $(this).attr('id').split('-')[3];
                $.notify('You have removed your source "' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['provider'] + '" on the widget "' + pages[page]['widgets'][windex]['title'] + '".', "success");
                pages[page]['widgets'][windex]['sources'].splice(sindex, 1);
                $('#' + widget['id'] + ' #' + windex + '-' + sindex + "-source-item").remove();
                displayWidgets(pages[page]['widgets']);
            });

            $('#' + widget['id'] + ' #' + windex + '-remove-page').click(function(e) {
                var windex = $(this).attr('id').split('-')[0];
                $('#' + pages[page]['widgets'][windex]['id']).remove();
                $.notify('You have removed the widget "' + pages[page]['widgets'][windex]['title'] + '".', "success");
                pages[page]['widgets'].splice(windex, 1);
                windowHeight = $(window).innerHeight();
                $('.page-content').css('min-height', windowHeight);
            });

            function panel_fullscreen(panel){

                if(panel.hasClass("panel-fullscreened")){
                    panel.removeClass("panel-fullscreened").unwrap();
                    panel.find(".panel-body,.chart-holder").css("height","");
                    panel.find(".panel-fullscreen .fa").removeClass("fa-compress").addClass("fa-expand");

                    $(window).resize();
                }else{
                    var head    = panel.find(".panel-heading");
                    var body    = panel.find(".panel-body");
                    var footer  = panel.find(".panel-footer");
                    var hplus   = 30;

                    if(body.hasClass("panel-body-table") || body.hasClass("padding-0")){
                        hplus = 0;
                    }
                    if(head.length > 0){
                        hplus += head.height()+21;
                    }
                    if(footer.length > 0){
                        hplus += footer.height()+21;
                    }

                    panel.find(".panel-body,.chart-holder").height($(window).height() - hplus);


                    panel.addClass("panel-fullscreened").wrap('<div class="panel-fullscreen-wrap"></div>');
                    panel.find(".panel-fullscreen .fa").removeClass("fa-expand").addClass("fa-compress");

                    $(window).resize();
                }
            }

            $(".panel-fullscreen").on("click",function(){
                panel_fullscreen($(this).parents(".panel"));
                return false;
            });

            $("#" + windex + "-btn-new-data-source").click(function (e) {
                var windex = e.target.id.split('-')[0];
                var dataset = $('#' + widget['id'] + ' #' + windex + '-plus-dataset').val();
                if(dataset != 'none') {
                    var windex = $(this).attr('id').split('-')[0];
                    pages[page]['widgets'][windex]['sources'].push(
                        {
                         "id": $("#"+ windex + "-plus-dataset").val(),
                         "aggregation": $("#"+ windex + "-plus-aggregation").val(),
                         "granularity": $("#"+ windex + "-plus-granularity").val(),
                         "chart": $("#"+ windex + "-plus-type").val(),
                         "type": "points",
                         "keyword": $("#"+ windex + "-plus-keyword").val(),
                         "start": start_date,
                         "end": end_date,
                         "dataset": null,
                         "markers": null
                    });
                    $('.' + windex + '-source-list').empty();
                    $('.' + windex + '-source-list').append('<div class="row">' +
                                        '<div class="high-name header-column col-md-2">' + 'Data' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'Source' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'From' + '</div>' +
                                        '<div class="high-name header-column col-md-2">' + 'To' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'Filtered by' + '</div> ' +
                                        '<div class="high-name header-column col-md-1"> ' + 'Commands' +  '</div> ' +
                                    '</div>');
                    pages[page]['widgets'][windex]['sources'].forEach(function(source, sindex){
                        $('.' + windex + '-source-list').append(
                            '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                '</div> ' +
                            '</div>'
                        );
                    });
                    $("#" + windex + "-modal").modal().hide();
                    displayWidgets(pages[page]['widgets']);
                    pages[page]['widgets'][windex]['modified'] = (new Date()).toISOString();
                    $('#' + widget['id'] + ' #' + windex + '-modified').html(pages[page]['widgets'][windex]['modified']);
                    $.notify('You have inserted a data source.', "success");
                }
                else {
                    $("#" + windex + "-modal").modal().hide();
                }
            });

            widget['sources'].forEach(function(source, sindex){

                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-dataset').on('change', function () {
                    var optionindex = $(this).val();
                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[optionindex]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[optionindex]['end']==null? 'now': moment(datasets[optionindex]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                        '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[optionindex]['language'] + '</span>. </div>');
                });

                $("#" + windex + "-" + sindex + "-edit-time-interval").daterangepicker({
                    ranges: {
                       'Today': [moment(), moment()],
                       'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                       'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                       'This Month': [moment().startOf('month'), moment().endOf('month')],
                       'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                    },
                    opens: 'left',
                    buttonClasses: ['btn btn-default'],
                    applyClass: 'btn-small btn-primary',
                    cancelClass: 'btn-small',
                    format: 'DD.MM.YYYY',
                    separator: ' to ',
                    startDate: moment().subtract('days', 6),
                    endDate: moment()
                  },function(start, end) {
                    pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                    pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                    $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                });
                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));

                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-modify').click(function(e) {
                    var windex = $(this).attr('id').split('-')[0];
                    var sindex = $(this).attr('id').split('-')[1];
                    var source = pages[page]['widgets'][windex]['sources'][sindex];
                    $("#" + windex + "-" + sindex + "-edit-dataset").val(source['id']);
                    $("#" + windex + "-" + sindex + "-edit-time-interval").val(source['date']);
                    $("#" + windex + "-" + sindex + "-edit-type").val(source['chart']);
                    $("#" + windex  + "-" + sindex+ "-edit-granularity").val(source['granularity']);
                    $("#" + windex  + "-" + sindex+ "-edit-aggregation").val(source['aggregation']);
                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[source['id']]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[source['id']]['end']==null? 'now': moment(datasets[source['id']]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                        '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[source['id']]['language'] + '</span>. </div>');
                });
            });

            $("#" + windex + "-sub-widget").click(function(e) {
                $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                $("#" + windex + "-slider-date-graph").hide()
                pages[page]['widgets'][windex]["highmarker"].forEach(function(highmarker, hindex){
                    highmarker.setIcon(pages[page]['widgets'][windex]["highmarkericon"][hindex]);
                    pages[page]['widgets'][windex]["highmarker"] = [];
                    pages[page]['widgets'][windex]["highmarkericon"] = [];
                    pages[page]['widgets'][windex]['data'] = [];
                });
            });


            $('.widget-title').dblclick(function(){
                old = $(this).text();
                $(this).html('<input class="input-widget-title" type="text" name="search" value=""/>');
                $('.input-widget-title').keypress(function (e) {
                   var key = e.which;
                   var id = $(this);
                   if(key == 13) {
                        if($(this).val() == '') {
                            $(this).parent().html('Blank title');
                            pages[id]['name'] = $(this).val();
                        }
                        else {
                            $(this).parent().html($(this).val());
                            pages[id]['name'] = $(this).val();
                        }
                   }
                });
            });

            if (widget['sources'].length > 0) {
                widget['sources'].forEach(function(source, sindex){
                   initialize_map(windex, sindex);
                    $("#" + widget['id'] + "-slider-button-step").click(function() {
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                        $("#" + windex + "-slider-date-graph").hide()
                        update_map(windex, sindex, +1);
                    });
                    $("#" + widget['id'] + "-slider-button-back").click(function() {
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                        $("#" + windex + "-slider-date-graph").hide()
                        update_map(windex, sindex, -1);
                    });
                    $("#" + widget['id'] + "-slider-button").click(function() {
                        $("#" + widget['id'] + "-slider-button").toggleClass('fa-play fa-pause');
                        if($("#" + widget['id'] + "-slider-button").hasClass("fa-play")) {
                            clearInterval(pages[page]['widgets'][windex]["refreshIntervalId"]);
                        }
                        else {
                            pages[page]['widgets'][windex]["refreshIntervalId"] = setInterval(function() { update_map(windex, sindex) }, 1000);
                            pages[page]['widgets'][windex]["highmarker"] = [];
                            pages[page]['widgets'][windex]["highmarkericon"] = [];
                            $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                            $("#" + windex + "-slider-date-graph").hide()
                        }
                    });



                    widget['sources'].forEach(function(source, sindex){
                        if($("#" + windex + "-" + sindex + "-edit-time-interval").length > 0){
                            $("#" + windex + "-" + sindex + "-edit-time-interval").daterangepicker({
                                ranges: {
                                   'Today': [moment(), moment()],
                                   'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                                   'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                                   'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                                   'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                                },
                                opens: 'left',
                                buttonClasses: ['btn btn-default'],
                                applyClass: 'btn-small btn-primary',
                                cancelClass: 'btn-small',
                                format: 'DD.MM.YYYY',
                                separator: ' to ',
                                startDate: moment().subtract('days', 6),
                                endDate: moment()
                              },function(start, end) {
                                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                                pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                                pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                            });
                        }
                        $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));
                     });

                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-close').click(function(e){
                        var windex = $(this).attr('id').split('-')[0];
                        var sindex = $(this).attr('id').split('-')[1];
                        var source = pages[page]['widgets'][windex]['sources'][sindex];
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        pages[page]['widgets'][windex]['sources'][sindex]['name'] = $("#"+ windex + "-" + sindex + "-edit-dataset").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['chart'] = $("#"+ windex + "-" + sindex + "-edit-type").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] = $("#"+ windex + "-" + sindex + "-edit-aggregation").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['granularity'] = $("#"+ windex + "-" + sindex + "-edit-granularity").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['keyword'] = $("#" + windex + "-" + sindex + "-edit-keyword").val().toLowerCase();
                        pages[page]['widgets'][windex]['sources'][sindex]['markers'].clearLayers();

                        $('.' + windex + '-source-list').empty();
                        pages[page]['widgets'][windex]['sources'].forEach(function(source, sindex){
                            $('.' + windex + '-source-list').append(
                                '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                    '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                    '</div> ' +
                                '</div>'
                            );
                        });


                        $('.remove').click(function(e) {
                            var windex = $(this).attr('id').split('-')[1];
                            var sindex = $(this).attr('id').split('-')[3];
                            pages[page]['widgets'][windex]['sources'].splice(sindex, 1);
                            $('#' + widget['id'] + ' #' + windex + '-' + sindex + "-source-item").remove();
                            displayWidgets(pages[page]['widgets']);
                        });

                        widget['sources'].forEach(function(source, sindex){
                            if($("#" + windex + "-" + sindex + "-edit-time-interval").length > 0){
                                $("#" + windex + "-" + sindex + "-edit-time-interval").daterangepicker({
                                    ranges: {
                                       'Today': [moment(), moment()],
                                       'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                                       'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                                       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                                       'This Month': [moment().startOf('month'), moment().endOf('month')],
                                       'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                                    },
                                    opens: 'left',
                                    buttonClasses: ['btn btn-default'],
                                    applyClass: 'btn-small btn-primary',
                                    cancelClass: 'btn-small',
                                    format: 'DD.MM.YYYY',
                                    separator: ' to ',
                                    startDate: moment().subtract('days', 6),
                                    endDate: moment()
                                  },function(start, end) {
                                    pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                                    pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                                    $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                                });
                                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));

                            }


                            $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-modify').click(function(e) {
                                var windex = $(this).attr('id').split('-')[0];
                                var sindex = $(this).attr('id').split('-')[1];
                                var source = pages[page]['widgets'][windex]['sources'][sindex];
                                $("#" + windex + "-" + sindex + "-edit-dataset").val(source['id']);
                                $("#" + windex + "-" + sindex + "-edit-time-interval").val(source['date']);
                                $("#" + windex + "-" + sindex + "-edit-type").val(source['chart']);
                                $("#" + windex  + "-" + sindex+ "-edit-aggregation").val(source['aggregation']);
                                $("#" + windex  + "-" + sindex+ "-edit-granularity").val(source['granularity']);
                                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[source['id']]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[source['id']]['end']==null? 'now': moment(datasets[source['id']]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                                    '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[source['id']]['language'] + '</span>. </div>');
                            });
                        });

                        pages[page]['widgets'][windex]['modified'] = (new Date()).toISOString();
                        $('#' + widget['id'] + ' #' + windex + '-modified').html(pages[page]['widgets'][windex]['modified']);
                        displayWidgets(pages[page]['widgets']);
                    });
                });
            }
            else {
                $("#" + pages[page]['widgets'][windex]['id'] + "-loader").hide();
                $("#" + pages[page]['widgets'][windex]['id'] + "-slider-button").show();
            }
        });
    }

    /* Loading Minimization */
    $(".x-navigation-minimize").on("click",function(){
        setTimeout(function(){
            rdc_resize();
        },200);
    });

    $('.dashboard-page').click(function(){
        var element = this;
        var t0 = new Date();
        if (t0 - doubleClickTime > threshold) {
            setTimeout(function () {
                if (t0 - doubleClickTime > threshold) {
                    doDashboardPageOnClick(element);
                }
            },threshold);
        }
    });

    $('.dashboard-page').dblclick(function(e){
        onDashboardPageDoubleClick(this);
    });

    $('.add').click(function(event){
        var id = Object.keys(pages).length + 1;
        $('<li id="page-' + id + '" class="dashboard-page" ondrop="drop(event)" ondragover="allowDrop(event)"> New Dashboard Page </li>').insertBefore(this);
        pages['page-'+id] = {};
        pages['page-'+id]['name'] = 'New Dashboard Page';
        pages['page-'+id]['widgets'] = [];


        $('.dashboard-page').click(function(){
            var element = this;
            var t0 = new Date();
            if (t0 - doubleClickTime > threshold) {
                setTimeout(function () {
                    if (t0 - doubleClickTime > threshold) {
                        doDashboardPageOnClick(element);
                    }
                },threshold);
            }
        });

        $('.dashboard-page').dblclick(function(e){
            onDashboardPageDoubleClick(this);
        });

        $.notify('You have inserted a dashboard page.', "success");
    });

    if(typeof new_shared_widget == 'undefined' && typeof new_shared_widgets == 'undefined') {
        page = "page-3";
        $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
        shareDashboard();
        $('#' + page).addClass('active');
        displayWidgets(pages[page]['widgets']);
    }
    else {
        var id = Object.keys(pages).length + 1;
        $('<li id="page-' + id + '" class="dashboard-page" ondrop="drop(event)" ondragover="allowDrop(event)"> Shared Dashboard Page </span> </li>').insertBefore('.add');
        pages['page-'+id] = {};
        pages['page-'+id]['name'] = 'New Dashboard Page';
        if(typeof new_shared_widgets == 'undefined') {
            pages['page-'+id]['widgets'] = [];
            pages['page-'+id]['widgets'].push(JSON.parse(new_shared_widget));
        }
        else {
            pages['page-'+id]['widgets'] = JSON.parse(new_shared_widgets)['widgets'];
        }

        $('.dashboard-page').dblclick(function(e){
            onDashboardPageDoubleClick(this);
        });

        $('.dashboard-page').click(function(){
            var element = this;
            var t0 = new Date();
            if (t0 - doubleClickTime > threshold) {
                setTimeout(function () {
                    if (t0 - doubleClickTime > threshold) {
                        doDashboardPageOnClick(element);
                    }
                },threshold);
            }
        });

        page = "page-" + id;
        $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
        shareDashboard();
        $('#' + page).addClass('active');
        displayWidgets(pages[page]['widgets']);
    }

    function doDashboardPageOnClick(element) {
        if (!$('.input-dashboard-page').length) {
            pages[page]['widgets'].forEach(function(widget, windex){
                clearInterval(pages[page]['widgets'][windex]["refreshIntervalId"]);
            });
            $('.dashboard-page').removeClass('active');
            $(element).addClass('active');
            $(".page-content-wrap").empty();
            page = $(element).attr('id');
            if (page == 'page-0') {
                pages[page] = {
                    "name": "Create New Widget",
                    "widgets": [
                        {
                            "id": "widget-6656",
                            "title": "New widget",
                            "authors": ["carmen"],
                            "modified": "2018-01-12T00:00:00Z",
                            "sources": [],
                            "timeinterval": null,
                            "map": null,
                            "highmarkericon": [],
                            "refreshIntervalId": null,
                            "highmarker": [],
                            "data": []
                        }
                        ]
                        }
            }
            $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
            shareDashboard();
            displayWidgets(pages[$(element).attr('id')]['widgets']);
            windowHeight = $(window).innerHeight();
            $('.page-content').css('min-height', windowHeight);
        }
    }

    function onDashboardPageDoubleClick(element) {
        doubleClickTime = new Date();
        old = $(element).text().trim();
        $(element).html('<input class="input-dashboard-page" type="text" name="search" value="' + old + '"/>');
        $('.input-dashboard-page').keypress(function (e) {
           var key = e.which;
           var id = $(this).parent().attr('id');
           if(key == 13) {
                if($(this).val() == '') {
                    $.notify('You have removed the dashboard page.', "success");
                    $(this).parent().remove();
                    delete pages[id];
                }
                else {
                    $(this).parent().html($(this).val());
                    $.notify('You have changed the dashboard name.', "success");
                    pages[id]['name'] = $(this).val();
                    $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
                }
           }
        });
    }

});